import java.awt.{Color, Graphics, Canvas}

/**
 * Created by ss7n13 on 10/07/15.
 */
class MyCanvas(SIZE: Int, PX: Int) extends Canvas {
  var fd = Array(Array(0))

  override def paint(g: Graphics) {
    g.setColor(Color.white)
    g.fillRect(0, 0, SIZE*PX, SIZE*PX)

    var x = 0
    var y = 0
    for (row <- fd) {
      for (pt <- row) {
        if (pt == 1) g.setColor(Color.black)
        else g.setColor(Color.white)
        g.fillRect(x * PX, y * PX, (x + 1) * PX, (y + 1) * PX)
        x += 1
      }
      x = 0
      y += 1
    }
    //    drawGrid(g)
  }

  def update(field: Array[Array[Int]]) = {
    fd = field
    repaint()
  }

  def drawGrid(g: Graphics) = {
    g.setColor(Color.black)
    (1 to SIZE) foreach(x =>
      g.drawLine(x * PX, 0, x * PX, getHeight))
    (1 to SIZE) foreach(y =>
      g.drawLine(0, y * PX, getWidth, y * PX))
  }
}