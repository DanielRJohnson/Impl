(startfigure 21 21)

(for i :in (range 1 21 2) 
	(setline :x i '(255 0 0))
)

(for i :in (range 1 21 2) 
	(setline :y i '(255 0 0))
)

(save "setline.png")
