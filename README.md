<h1> Visualising NHL winning and losing streaks </h1>

<h2> Check it online </h2>

<a href="http://hamatti.org/nhl/nhl-streak.html"> Demo </a>

<h2> Background </h2>

Ice hockey and NHL have always been my favourites and this season Chicago Blackhawk's almost broke records for longest non-losing streak in the NHL and it motivated me to check out how other teams were doing.

<h2> Usage </h2>

<ol>
<li> Check the <a href="http://www.nhl.com/ice/gamestats.htm?fetchKey=20132ALLSATAll&viewName=summary&sort=gameDate">NHL page</a> for current number of pages and change the PAGENUMBER constant to that (this will be fixed in the next update).</li>
<li> <i>python nhl.py [--web] [--json] [--html]</i>
     <ul>
     <li> --web: load the data from the web (if not set, will read from JSON)</li>
     <li> --json: write the data to JSON file </li>
     <li> --html: write the html file </li>
     </ul>
</li>
<li> <i> ./nhl.sh </i> will combine the header file, footer file and the contents created by the python script. </li>

</ol>

<h2> Licence </h2>
Copyright (C) 2013 Juha-Matti Santala

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

<h2> Contact </h2>
If you have ideas how to improve the script, feel free to fork it and make a pull request or you can contact me on Twitter @hamatti.