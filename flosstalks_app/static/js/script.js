/*
    This file is part of FLOSS Talks.

    FLOSS Talks is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    FLOSS Talks is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with FLOSS Talks.  If not, see <http://www.gnu.org/licenses/>.
*/

//Initialize the Typeahead in the navbar and on the search page
$.getJSON("/search-values.json", function(data) {
    $('.typeahead').typeahead({
        source: data
    });
});
