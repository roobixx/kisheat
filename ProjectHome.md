kisheat.py is a tool that renders temperature-map style overlays for google earth etc from your kismet "war driving" data.

<img src='https://lh4.googleusercontent.com/-ZYciwcb-dg0/TuV0oFQsFVI/AAAAAAAAAmg/cPdrKBZe9Po/s1280/samplemap.png'>

<pre>
Usage: [options] [path/to/]SAMPLE_NAME [ESSID PATTERN]<br>
<br>
Options:<br>
-h, --help            show this help message and exit<br>
-l, --list            Just list xSSIDs and exit<br>
-a, --alldata         Include all samples taken while not moving (can<br>
exaggerate signal strength)<br>
-m MERGETO, --mergedata=MERGETO<br>
Merge all datasets into one overlay whose name you<br>
must specify.  If you use a regex filter the merged<br>
data will be restricted to accesspoints that matched<br>
it.  Useful for whole-network coverage mapping.<br>
</pre>

To install kisheat.py, check out the source from the repository<br>
and follow instructions in the README file.<br>
<br>
<br>
kisheat owes its existence to:<br>
<br>
<p>Kismet:               <a href='http://www.kismetwireless.net'>http://www.kismetwireless.net</a></p>
<p>Heatmap.py library:   <a href='http://jjguy.com/heatmap/'>http://jjguy.com/heatmap/</a></p>
<p>Heatmap.py patch:     <a href='http://alexlittle.net/blog/tag/heatmap-py/'>http://alexlittle.net/blog/tag/heatmap-py/</a></p>