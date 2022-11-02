(startfigure 16 16)

(define redcounter 0)

(for i :in (range 16)
	(for j :in (range 16)
		(do
			(setpixel (list j i) :to (list redcounter 0 0))
			(set! redcounter (+ redcounter 1))
			(snap!)
		)
	)
)

(save "snap.gif")