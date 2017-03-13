Rush Hour
=========

Classic Rush hour game. More info on [wiki](https://en.wikipedia.org/wiki/Rush_Hour_(board_game))



Input
-----

Input is the 6x6 board. 'rr' is usually the red car. And use other letters to indicate other cars. Input is passed in *stdin*.

For example

	...IJJ
	...IEF
	GGHHEF
	rr..EF
	..BBCC
	....AA

Output
------

The output is the series of moves to solve the problem. 

	r-Right
	r-Right
	B-Left
	B-Left
	C-Left
	C-Left
	A-Left
	A-Left
	E-Down
	E-Down
	H-Right
	F-Down
	F-Down
	H-Right
	I-Down
	J-Left
	J-Left
	J-Left
	I-Up
	H-Left
	H-Left
	E-Up
	E-Up
	E-Up
	r-Right
	F-Up
	F-Up
	F-Up
	r-Right

If you change the parameter in `print_path` function it'll show you the board after each move


Notes
-----

1. Its possible to feed bigger board. But its written in python and not very optimized, so it may not finish.
2. The exit path of red car is always the right most column in the same row
3. It only allowes red car to be in horizontal position
