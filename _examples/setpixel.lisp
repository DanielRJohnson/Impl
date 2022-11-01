(startfigure 16 16)

(for i :in (range 0 16)
	(setpixel (list i i) :to '(255 0 0))	
)

(save "setpixel.png")