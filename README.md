# PolyPy

I saw a video about polyrhythms and I want do something like that with Python

- Draw shapes
    - [X] Line animation
    - [X] N points animation
        - interior angle = (180 * (n-2)) n
        - Xi = Xo + d * cos(i * angle)
        - Yi = Yo + d * sin(i * angle)
    - [X] Circle animation
    - [X] Flip Figures (upsidown)
    - [X] Speed should be dependent on vertex count
        When changing the speed the collision logic breaks :panik:
    - [] Speed over BPM X = Xo + d * (BPM/60) * t
    - [] Glow (blip flags)
- [X] Audio
    - [] Samples?
    - [] Different waves
    - [] ADSR
    - [] Sample
- [] Distance, speed, BPMs

- [] Harmonics: (-1)k * (sin(2pi * k * ft)) / 2k - 1 || ft=fundamental frec | k = num of frecs
https://www.youtube.com/watch?v=Y7TesKMSE74


## Different speeds
The problem with different speeds is that I need to consider rounding problems, if I say that the line is t1 when I
use the square it works just fine because I do t*2,  distance is the same but doubled. For t3 distances is not quite the 
same because when the line reaches 0 the triagle reaches `dist: 16.0 - speed: 12 | hit | dist: 4.0 - speed: 12`.
Clever solution! just rest the inverse leftover vector to the new position and profit!