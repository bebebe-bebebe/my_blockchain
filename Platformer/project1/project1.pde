Sprite бобик;
PImage box_block;
PImage brown_block;
PImage grass_dirt_block;
PImage red_block;
ArrayList<Sprite> platforms;
final static float SPRITE_SIZE = 50;
final static float SPRITE_SCALE = SPRITE_SIZE / 128;
final static float MOVE_SPEED = 2;

// Переменные для камеры
float cameraX = 0;
float cameraY = 0;

void setup() {
  size(800, 600);
  бобик = new Sprite("img/бобик.png", 100, 100, 1);
  box_block = loadImage("img/box_block.png");
  brown_block = loadImage("img/brown_block.png");
  grass_dirt_block = loadImage("img/grass_dirt_block.png");
  red_block = loadImage("img/red_block.png");
  бобик.set_step_x(0);
  бобик.set_step_y(0);
  бобик.set_pos_x(100);
  бобик.set_pos_y(100);
  platforms = new ArrayList<Sprite>();
  createPlatforms("img/map.csv"); // Загружаем платформы из файла
}

void draw() {
  background(255, 255, 255);
  
  // Обновляем смещение камеры
  updateCamera();
  
  // Отображаем все объекты с учетом смещения камеры
  pushMatrix();
  translate(-cameraX, -cameraY);
  
  // Отображаем платформы
  for (Sprite platform : platforms) {
    platform.show();
  }
  
  // Отображаем персонажа
  бобик.show();
  бобик.update_pos();
  
  popMatrix();
}

void keyPressed() {
  if (keyCode == RIGHT) {
    бобик.set_step_x(MOVE_SPEED);
  } else if (keyCode == LEFT) {
    бобик.set_step_x(-MOVE_SPEED);
  } else if (keyCode == UP) {
    бобик.set_step_y(-MOVE_SPEED); // Движение вверх
  } else if (keyCode == DOWN) {
    бобик.set_step_y(MOVE_SPEED);
  }
}

void keyReleased() {
  if (keyCode == RIGHT || keyCode == LEFT) {
    бобик.set_step_x(0); // Останавливаем движение по горизонтали
  } else if (keyCode == UP || keyCode == DOWN) {
    бобик.set_step_y(0); // Останавливаем движение по вертикали
  }
}

void createPlatforms(String filename) {
  String[] lines = loadStrings(filename);
  for (int row = 0; row < lines.length; row++) {
    String[] cells = split(lines[row], ";");
    for (int col = 0; col < cells.length; col++) {
      if (cells[col].equals("1")) {
        Sprite sprite = new Sprite(box_block, SPRITE_SCALE);
        sprite.set_pos_x(col * SPRITE_SIZE); // Позиция платформы по X
        sprite.set_pos_y(row * SPRITE_SIZE); // Позиция платформы по Y
        platforms.add(sprite); // Добавляем спрайт в список платформ
      }
      if (cells[col].equals("2")) {
        Sprite sprite = new Sprite(grass_dirt_block, SPRITE_SCALE);
        sprite.set_pos_x(col * SPRITE_SIZE); // Позиция платформы по X
        sprite.set_pos_y(row * SPRITE_SIZE); // Позиция платформы по Y
        platforms.add(sprite); // Добавляем спрайт в список платформ
      }
      if (cells[col].equals("3")) {
        Sprite sprite = new Sprite(brown_block, SPRITE_SCALE);
        sprite.set_pos_x(col * SPRITE_SIZE); // Позиция платформы по X
        sprite.set_pos_y(row * SPRITE_SIZE); // Позиция платформы по Y
        platforms.add(sprite); // Добавляем спрайт в список платформ
      }
      if (cells[col].equals("4")) {
        Sprite sprite = new Sprite(red_block, SPRITE_SCALE);
        sprite.set_pos_x(col * SPRITE_SIZE); // Позиция платформы по X
        sprite.set_pos_y(row * SPRITE_SIZE); // Позиция платформы по Y
        platforms.add(sprite); // Добавляем спрайт в список платформ
      }
    }
  }
}

void updateCamera() {
  // Центрируем камеру на персонаже
  cameraX = бобик.get_pos_x() - width / 2;
  cameraY = бобик.get_pos_y() - height / 2;
  
  // Ограничиваем камеру, чтобы она не выходила за пределы карты
  float mapWidth = platforms.size() * SPRITE_SIZE; // Ширина карты
  float mapHeight = platforms.size() * SPRITE_SIZE; // Высота карты
  
  cameraX = constrain(cameraX, 0, mapWidth - width);
  cameraY = constrain(cameraY, 0, mapHeight - height);
}

boolean checkCollision(Sprite sprite1, Sprite sprite2){
  boolean noXCross = sprite1.getRight()<=sprite2.getLeft() || sprite1.getRight()>=sprite2.getLeft() ;
  boolean noYCross = sprite1.getBottom()<=sprite2.getTop() || sprite1.getBottom()>=sprite2.getTop();
  if (noXCross || noYCross){
    return false;
  }else{
    return true;
  }
}
public ArrayList<Sprite> checkCollisionList(Sprite sprite, ArrayList<Sprite> lsit){
  ArrayList<Sprite> collision_list = new ArrayList<Sprite>();
  for(Sprite s: list){
    if(checkCollision(sprite,s)){
      collisions_list.add(s);
    }
  }
  return collisions_list;
}
