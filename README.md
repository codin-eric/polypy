# PolyPy

I saw a video about polyrhythms and I want do something like that with Python

- Bugs
    - [] Diagonal speeds are faster than pure x or y. Problem with the speed formula, maybe calculate top speed and use angle to solve for x y components. I also need to do Speed over BPMs?
        - [] Speed over BPM X = Xo + d * (BPM/60) * t
    - [] collision distance is hardcoded
- Draw shapes
    - [x] Line animation

    - [X] N points animation
        - interior angle = (180 * (n-2)) n
        - Xi = Xo + d * cos(i * angle)
        - Yi = Yo + d * sin(i * angle)
    - [] Circle animation
    - [] Glow (blip flags)
- [x] Audio
    - [] Different waves
    - [] ADSR
    - [] Sample
- [] Distance, speed, BPMs

- [] Harmonics: (-1)k * (sin(2pi * k * ft)) / 2k - 1 || ft=fundamental frec | k = num of frecs
https://www.youtube.com/watch?v=Y7TesKMSE74
