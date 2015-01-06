#set terminal wxt noraise persist size 800,800 background '#000000' enhanced font 'Consolas,10' 

set terminal pngcairo size 1200,800 background '#000000' enhanced font 'Consolas,10'
set output "graph.png"

#set key outside

set style line 99 linecolor rgb "#ffffff" linetype 0 linewidth 2

set xlabel "Time" textcolor linestyle 99
set ylabel "Degrees C"  textcolor ls 99
set title "Room temperature" textcolor ls 99

set key top right textcolor linestyle 99 
set grid linestyle 99
set border linestyle 99

set xdata time
set timefmt "%Y-%m-%d-%H:%M:%S"
set format x "%H:%M:%S"

plot filename using 1:($2/1000) title "Temperature" w l, \
     filename using 1:($2/1000) title "Temperature (smoothed)" smooth sbezier
	 
