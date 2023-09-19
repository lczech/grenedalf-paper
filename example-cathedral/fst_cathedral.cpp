/*
    Genesis - A toolkit for working with phylogenetic data.
    Copyright (C) 2014-2023 Lucas Czech

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Contact:
    Lucas Czech <lczech@carnegiescience.edu>
    Department of Plant Biology, Carnegie Institution For Science
    260 Panama Street, Stanford, CA 94305, USA
*/

#include "genesis/genesis.hpp"

#include <algorithm>
#include <bitset>
#include <cassert>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <functional>
#include <iomanip>
#include <string>
#include <unordered_map>

using namespace genesis;
using namespace genesis::population;
using namespace genesis::utils;

// Input data
std::string const infile = "/home/lucas/Dropbox/GitHub/grenedalf/counts.sync";
size_t const length = 30427671;
size_t const poolsize = 100;

// =================================================================================================
//     Compute Matrix
// =================================================================================================

Matrix<double> compute_matrix( size_t height, size_t width )
{
    struct FST
    {
        FST( size_t pos_, double pi_w_, double pi_t_ )
            : pos( pos_ )
            , pi_w( pi_w_ )
            , pi_t( pi_t_ )
        {}

        size_t pos;
        double pi_w = 0.0;
        double pi_t = 0.0;
        // double pi_b_sum_ = 0.0;
    };

    // Store all fst values for the whole thing.
    std::vector<FST> fsts;

    // Iterate the input sync file line by line, with a simple counts filter.
    auto data_iterator = make_variant_input_iterator_from_sync_file( infile );

    // Process that data stream in sliding windows.
    auto window_iterator = make_default_sliding_interval_window_iterator(
        data_iterator.begin(), data_iterator.end(), 1
    );

    // Go through all snps and compute their fst.
    LOG_DBG << "windows";
    for( auto const& window : window_iterator ) {
        // Compute fst in the window.
        auto fst_calc = FstPoolCalculatorUnbiased( poolsize, poolsize );
        size_t pos = 0;
        for( auto const& var : window ) {
            fst_calc.process( var.data.samples[0], var.data.samples[1] );
            pos = var.position;
        }
        if( pos > 0 ) {
            fsts.push_back( FST{ pos, fst_calc.get_pi_within(), fst_calc.get_pi_total() });
        }
    }
    LOG_DBG << "fsts.size()=" << fsts.size();

    // Compute the results matrix
    LOG_DBG << "matrix";
    size_t total_count = 0;
    auto result = Matrix<double>( height, width );
    auto snp_count = Matrix<size_t>( height, width );
    for( size_t row = 0; row < height; ++row ) {
        // LOG_DBG1 << "row=" << row;

        double const len_d = static_cast<double>( length );
        auto const row_val = row + 1;

        // Geometric window length
        // double const pieces = static_cast<double>( row_val );
        // double const window_width = len_d / pieces;
        // LOG_DBG1 << "At row " << row_val << " with pieces=" << pieces << " and window_width=" << window_width;

        // Linear interpolated window length
        // minimum width of windows, where each window corresponds to one pixel of width,
        // and max width, corresponding to whole genome as one window
        auto const min_win_width = len_d / static_cast<double>(width);
        auto const max_win_width = len_d;
        // // how far in the rows are we, percentage
        // auto const row_frac = static_cast<double>(row) / static_cast<double>(height);
        // // interplate linearly between min and max window width
        // auto const window_width = (max_win_width - min_win_width) * (1.0 - row_frac) + min_win_width;


        // Exponential decay
        auto const decay = - std::log( 1.0 / static_cast<double>(width)) / static_cast<double>(height-1);
        auto const window_width = len_d * std::exp(-decay * static_cast<double>(row) );
        auto const advance = len_d /  static_cast<double>(width);

        if( row == 0 ) {
            LOG_DBG << "min_win_width=" << min_win_width << " max_win_width=" << max_win_width;
            LOG_DBG << "decay=" << decay << " advance=" << advance;
        }
        LOG_DBG1 << "At row " << row_val << " with window_width=" << window_width;

        auto covered = Bitvector( fsts.size() );

        double index = - window_width / 2.0;
        for( size_t col = 0; col < width; ++col ) {
            assert( index + window_width >= 0.0 );
            auto lpos = static_cast<size_t>( std::max( index, 0.0 ));
            auto rpos = std::min( static_cast<size_t>(index + window_width), length );
            if( col == width - 1 ) {
                rpos = length;
            }
            index += advance;
            // LOG_DBG2 << "lpos=" << lpos << " rpos=" << rpos << " index=" << index;

            // Find which entries to use
            auto const it = std::lower_bound(
                fsts.begin(), fsts.end(), lpos,
                []( FST const& e, double v ){
                    return e.pos < v;
                }
            );
            size_t const b = std::distance( fsts.begin(), it );
            size_t i = b;
            assert( i <= fsts.size() );
            assert( i == fsts.size() || fsts[i].pos >= lpos );
            assert( i == 0 || fsts[i-1].pos < lpos );

            // Sum up the fst parts
            double pi_w_sum = 0.0;
            double pi_t_sum = 0.0;
            while( i < fsts.size() && fsts[i].pos <= rpos ) {
                // The actual positions between which we have the highest fst
                // if( fsts[i].pos == 14610295 ) {
                //     LOG_DBG2 << "reach 14610295 at " << col << " window " << lpos << "-" << rpos;
                // }
                // if( fsts[i].pos == 14610656 ) {
                //     LOG_DBG2 << "reach 14610656 at " << col << " window " << lpos << "-" << rpos;
                // }
                pi_w_sum += fsts[i].pi_w;
                pi_t_sum += fsts[i].pi_t;
                if( ! std::isfinite( fsts[i].pi_w )) {
                    LOG_WARN << "at " << row << ":" << col << " fsts[i].pi_w=" << fsts[i].pi_w;
                }
                if( ! std::isfinite( fsts[i].pi_t )) {
                    LOG_WARN << "at " << row << ":" << col << " fsts[i].pi_t=" << fsts[i].pi_t;
                }
                covered.set(i);
                ++i;
                ++snp_count( row, col );
                ++total_count;
            }
            // LOG_DBG2 << "b=" << b << " e=" << i;
            assert( i == fsts.size() || fsts[i].pos > rpos );

            result( row, col ) = 1.0 - ( pi_w_sum / pi_t_sum );
        }

        // TODO
        // center, round down and yp
    }

    LOG_DBG << "total_count=" << total_count;

    // Write result matrix
    MatrixWriter<double>().write( result, to_file( "matrix_proto.csv" ));
    // MatrixWriter<size_t>().write( snp_count, to_file( "snp_count.csv" ));

    return result;
}

// =================================================================================================
//     Main
// =================================================================================================

Matrix<double> read_matrix()
{
    return MatrixReader<double>().read( from_file(
        "/home/lucas/Dropbox/GitHub/genesis/bin/apps/matrix_proto.csv"
    ));
}

int main()
{
    // Activate logging.
    utils::Logging::log_to_stdout();
    utils::Logging::details.time = true;
    LOG_INFO << "Started";

    // Prepare result to contain values
    size_t const width = 1500;
    size_t const height = 250;
    // size_t const height = 100;

    // Compute matrix
    auto result = compute_matrix( height, width );
    // auto result = read_matrix();

    // Compute average fst across all cells, and max.
    auto const min_max_fst = matrix_minmax( result );
    LOG_DBG << "min_max_fst.min=" << min_max_fst.min;
    LOG_DBG << "min_max_fst.max=" << min_max_fst.max;

    LOG_DBG << "at 249:716 " << result(249,716);
    size_t nan_cnt = 0;
    for( auto& fst : result ) {
        if( ! std::isfinite(fst) ) {
            fst = 0.0;
            ++nan_cnt;
        }
    }
    LOG_DBG << "nan_cnt=" << nan_cnt;
    LOG_DBG << "at 249:716 " << result(249,716);

    // Turn into colors and store as bitmap
    // auto const color_scale = 5.0;
    auto const color_scale = 5.0;
    (void) color_scale;
    auto map = ColorMap( color_list_inferno() );
    // auto map = ColorMap( color_list_viridis() );
    map.clip( true );
    // map.mask_color( Color( 0,0,1 ));
    auto norm = ColorNormalizationLinear( 0.0, min_max_fst.max / color_scale );
    // auto norm = ColorNormalizationLogarithmic( 0.001, min_max_fst.max );
    auto image = Matrix<Color>( height, width );
    for( size_t row = 0; row < height; ++row ) {
        for( size_t col = 0; col < width; ++col ) {
            // if( ! std::isfinite( result(row, col) ) ) {
            //     LOG_DBG << "at " << row << ":" << col << " writing " << result( row, col ) << " as " << map( norm, result( row, col ));
            // }
            image( row, col ) = map( norm, result( row, col ));
        }
    }
    utils::BmpWriter().write( image, to_file( "image.bmp" ));

    // Make an x-axis
    auto x_axis_settings = SvgAxisSettings();
    x_axis_settings.position = SvgAxisSettings::Position::kBottom;
    x_axis_settings.length = width;
    auto const x_axis = make_svg_axis( x_axis_settings, Tickmarks().linear_labels( 1, length, 5 ), "Genome position");

    // TODO round the log labels! window sizes are doubles here, which does not look nice

    // Make a y-axis
    auto y_axis_settings = SvgAxisSettings();
    y_axis_settings.position = SvgAxisSettings::Position::kLeft;
    y_axis_settings.length = height;
    auto const min_win_width = static_cast<double>( length ) / static_cast<double>(width);
    auto const max_win_width = static_cast<double>( length );
    auto const y_axis = make_svg_axis(
        y_axis_settings, Tickmarks().logarithmic_labels(
            min_win_width, max_win_width, 10.0 //2.718282
        ),
        "Window size"
    );

    // Test
    auto const tm = Tickmarks().logarithmic_labels(
        min_win_width, max_win_width, 10.0 // 2.718282
    );
    for( auto const& t : tm ) {
        LOG_DBG << t.relative_position << " --> " << t.label;
    }

    // Make a color bar
    auto color_bar_settings = SvgColorBarSettings();
    color_bar_settings.height = height;
    auto const color_bar = make_svg_color_bar( color_bar_settings, map, norm );

    // Make an svg doc as well
    auto svg = GenomeHeatmap();
    svg.add( "Chromosome 1", image, x_axis, y_axis, color_bar );
    svg.write( to_file( "image.svg" ));

    LOG_WARN << "at 249:716 " << image(249,716);

    LOG_INFO << "Finished";
    return 0;
}
