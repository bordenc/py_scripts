#! /usr/bin/python3

def width_to_diagonal_height( width, x_res, y_res ):
	diagonal = ( width**2 * ( 1 + y_res**2 / x_res**2 ) )**0.5
	return diagonal, width * y_res / x_res

def diagonal_to_x_y( diagonal, x_res, y_res):
	width = ( diagonal**2 / ( 1 + y_res**2 / x_res**2 ) )**0.5
	return width, width * y_res / x_res