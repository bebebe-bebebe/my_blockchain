PImage img,img2;
float posX;
float posY;
float stepX;
float stepY;
float colorR=255, colorG=255, colorB=255;
int wScreen;
int hScreen;
void setup(){
  wScreen=500;
  hScreen=500;
  size(500,500);
  posX=1;
  posY=100;
  stepX=1;
  img = loadImage("бобик.png"); img2 = loadImage("бобик.png");
}
void draw(){
  background(colorR,colorG,colorB);
  image(img, posX,posY-150);
  image(img, wScreen-10,0);
  posX+=stepX;
  stepX+=0.01;
  posY+=stepY;
  stepY+=0.01;
  colorR-=1;
  colorG-=1;
  colorB-=1;
}
