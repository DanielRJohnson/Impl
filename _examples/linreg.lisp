(define DIM 512)
(startfigure DIM DIM)

;; CREATE MOCK DATASET
(define xs (range 100 (- DIM 100)))
(define ys (map (lambda (x) (+ x (randint -100 100))) xs))

;; VISUALIZE DATA
(for i :in (range (length xs))
	(setpixel (list (nth i xs) (- (- DIM 1) (nth i ys))) :to '(255 0 0))
)

;; DEFINE COST FUNCTION
(define RMSE (lambda (theta xs ys)
	(do
		(define sumerr 0)
		(define hx (map (lambda (x) (* x theta)) xs))
		(for i :in (range (length xs)) 
			(set! sumerr (+ sumerr (pow (- (nth i ys) (nth i hx)) 2)))
		)
		(set! sumerr (/ sumerr (length hx)))
		(sqrt sumerr)
	)
))

;; DEFINE COST FUNCTION'S DERIVATIVE
(define RMSE_der (lambda (theta xs ys) 
	(do
		(define dersum 0)
		(for i :in (range (length xs))
			;; dJ/dW = (2/m) * sum (theta*x - y)*x
			(set! dersum (* 
							(- 
								(* theta (nth i xs)) 
								(nth i ys)) 
							(nth i xs)))
		)
		(* dersum (/ 2 (length xs)))
	)
))

;; INITIALIZE HYPERPARAMS
(define theta 0)
(define n_iter 100)
(define alpha 0.0001)
(define theta_hist (list theta)) ;; Keep track of thetas

;; GRADIENT DESCENT
(for iter :in (range n_iter)
	(do
		(set! theta (- theta (* alpha (RMSE_der theta xs ys))))
		(set! theta_hist (append theta_hist (list theta)))
		(print "Training iteration:" iter "RMSE:" (RMSE theta xs ys))
	)
)

;; CREATE TRAINING ANIMATION
(print "Plotting...")
(for theta :in theta_hist 
	(do
		(define xs (range DIM))
		(define ys (map (lambda (x) (round (* x theta))) xs))
		(set! ys (map (lambda (y) (if (> y (- DIM 1)) (- DIM 1) y)) ys)) ;; keep in range
		(for i :in (range (length xs))
			(setpixel (list (nth i xs) (- (- DIM 1) (nth i ys))) :to '(0 0 255))
		)
		(snap!)
	)
)

(print "Saving...")
(save "linreg.gif")