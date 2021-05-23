/*
    Genesis - A toolkit for working with phylogenetic data.
    Copyright (C) 2014-2021 Lucas Czech

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

#include <fstream>
#include <string>
#include <map>

using namespace genesis;
using namespace genesis::population;
using namespace genesis::utils;

int main()
{
    // Activate logging.
    utils::Logging::log_to_stdout();
    utils::Logging::details.time = true;

    utils::Options::get().number_of_threads( 4 );
    // LOG_BOLD << utils::Options::get().info();
    // LOG_BOLD;

    for( size_t i = 1; i < 1000; ++i ) {
        auto d = static_cast<double>(i) / 10.0;
        try {
            auto a = alpha_star(d);
            auto b = beta_star(d);
            LOG_DBG << d << ", " << a << ", " << b;
        } catch(...) {
            LOG_DBG << d;
        }
    }

    return 0;
}
