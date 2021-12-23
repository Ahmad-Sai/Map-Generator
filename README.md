# Perlin-Noise

This program is a simple implementation of the Perlin Noise algorithim. The Perlin Noise algorithm is used to generate natural looking textures using noise.


Dependencies:
  - Math Module
  - Random Module
  - NumPy
  - MatPlotLib

Layer 1 generated with 8 boxes (least detail)
Layer 2 generated with 16 boxes (medium detail)
Layer 3 generated with 32 boxes (most detail)

Resulting layer sums all pervious layers to make a detailed image

![image](https://user-images.githubusercontent.com/85080576/147283377-c369e4a5-087d-4200-8dc5-4069851f29ce.png)

Example 1 was created using a small number of boxes (less detail and less noise)

Example 2 was created using a larger number of boxes (more detail and more noise)

![image](https://user-images.githubusercontent.com/85080576/147283513-83b94222-adfa-4e43-9499-dcdb39bf4bb1.png)

_Maps created using the perlin noise algorithim can be used to generate map terrians for video games._
