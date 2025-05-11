class Sprite {
  PImage img;
  float pos_x, pos_y;
  float step_x, step_y;
  float scale;
  float s_width;

  Sprite(String imagePath, float x, float y, float s) {
    img = loadImage(imagePath);
    pos_x = x;
    pos_y = y;
    scale = s;
    step_x = 0;
    step_y = 0;
  }

  Sprite(PImage image, float s) {
    img = image;
    scale = s;
    step_x = 0;
    step_y = 0;
  }

  void set_step_x(float step) {
    step_x = step;
  }

  void set_step_y(float step) {
    step_y = step;
  }

  void set_pos_x(float x) {
    pos_x = x;
  }

  void set_pos_y(float y) {
    pos_y = y;
  }

  // Добавляем методы для получения позиции
  float get_pos_x() {
    return pos_x;
  }

  float get_pos_y() {
    return pos_y;
  }

  void show() {
    imageMode(CENTER);
    image(img, pos_x, pos_y, img.width * scale, img.height * scale);
  }

  void update_pos() {
    pos_x += step_x;
    pos_y += step_y;
  }
  void setLeft(float left){
    pos_x = left +s_width/2;
  }
  void setRight(float right){
    pos_x = right - s_width/2;
  }
  public void setTop(float top){
    pos_y = top + s_height/2;
  }
  public void setBottom(float bottom){
    pos_y = bottom - s_height/2;
  }
  float getTop(){
    return top - s_width/2;
  }
  float getRight(){
    return pos_x + s_width/2;
  }
  float getLeft(){
    return pos_x - s_width/2;
  }
  float getBottom(){
    return bottom + s_width/2;
  }
