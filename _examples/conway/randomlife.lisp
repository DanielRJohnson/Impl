(define DIM 64)
(define ITERS 100)
(define cell_init_prob 0.15)
(startfigure DIM DIM)

;; Each cardinal direction including diagonals
(define directions 
	'(
		(-1 -1) (-1 0) (-1 1)
		(0 -1)         (0 1)
		(1 -1)  (1 0)  (1 1)
	)
)

;; Gets all neighbors in each direction provided they are in range
(define neighbors (lambda (i j) 
	(do
		(define ns_unsafe (map (lambda (dir) ;; add directions to position
			(list (+ i (nth 0 dir)) (+ j (nth 1 dir)))) directions))
		(filter (lambda (n) 
			(do
				(define i (nth 0 n))
				(define j (nth 1 n))
				(and (and (>= i 0) (>= j 0)) (and (< i DIM) (< j DIM)) )))
		ns_unsafe)
	)
))

;; Conway's Game of Life:
;;     Rules:
;;         If a pixel is alive:
;;             If it has two or three alive neighbors, it lives
;;             Else it dies
;;         If a pixel is not alive:
;;             If it has exactly three alive neighbors, it becomes alive
;;             Else it stays dead
;;
;; life takes in a previous board and returns the next iteration
(define life (lambda (prev) 
	(do
		(define next (map (lambda (l) (map (lambda (v) v) l)) prev )) ;; copy
		(for i :in (range DIM)
			(for j :in (range DIM)
				(do
					(define ns (neighbors i j))
					(define alive_ns (length (filter (lambda (n) (nth (nth 0 n) (nth (nth 1 n) prev))) ns)))
					(if (nth i (nth j prev)) ;; If the pixel is alive
						(if (not (or (= alive_ns 2) (= alive_ns 3))) ;; If it does not have 2 or 3 alive neighbors
							(list-set! (nth j next) i False) ;; pixel dies
							:pass ;; pixel lives
						)
						;; The pixel is dead
						(if (= alive_ns 3) ;; If it has exactly three alive neighbors
							(list-set! (nth j next) i True) ;; pixel becomes alive
							:pass ;; pixel stays dead
						) 
					) 
				)
			)
		)
		next ;; return next
	)
))

;; Create the simulation board, initialize to all False
(define sim (map (lambda (_) (* (list False) DIM)) (* (list False) DIM)))

;; Randomly set spaces to True in accordance with cell_init_prob
(for i :in (range DIM)
	(for j :in (range DIM)
		(list-set! (nth j sim) i (>= (uniform 0 1) (- 1 cell_init_prob)))
	)
)

;; Draws the given simulation board. True=Alive=Black, False=Dead=White
(define drawsim (lambda (s) 
	(for i :in (range DIM)
		(for j :in (range DIM)
			(if (nth i (nth j s))
				(setpixel (list i j) :to '(0 0 0)) ;; alive
				(setpixel (list i j) :to '(255 255 255)) ;; dead
			)
		)
	)
))

;; Run the simulation
(for iter :in (range ITERS)
	(do
		(print "Progress:" iter " / " ITERS)
		(drawsim sim)
		(snap!) ;; save animation frame
		(set! sim (life sim)) ;; advance the game
	)
)

(print "Saving...")
(save "randomlife.gif")