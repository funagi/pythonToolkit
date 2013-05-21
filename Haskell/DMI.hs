module Main where

	getLengthFromDMI :: (Floating a) => a -> a -> a
	getLengthFromDMI k j = 2.0 * pi / atan( k / sqrt(2.0) / j )

	getDMIFromLength :: (Floating a) => a -> a -> a
	getDMIFromLength d j = sqrt(2.0) * j * tan( 2.0 * pi / d )