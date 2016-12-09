import javax.swing.JFrame
import java.awt.Dimension

class Pointt(xc: Int, yc: Int) {
  val x: Int = xc
  val y: Int = yc

  override def toString():String = x + ", " + y
}

object GameOfLife {
  val SIZE = 100
  val PX =  5
  val DELAY = 50

  val frame = new JFrame("Game of Life")
  val cnvs = new MyCanvas(SIZE, PX)
  frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE)
  cnvs.setPreferredSize(new Dimension(SIZE*PX, SIZE*PX))
  frame.add(cnvs)
  frame.pack()
  frame.setVisible(true)

  def main(args: Array[String]): Unit = {
    var state = initialState()

    //TOAD
    //    state(5)(5) = 1;
    //    state(5)(6) = 1;
    //    state(5)(7) = 1;

    //GLIDER
    state(3)(3) = 1
    state(4)(4) = 1
    state(5)(2) = 1
    state(5)(3) = 1
    state(5)(4) = 1

    showNextState(state)
  }

  def display(field: Array[Array[Int]], canvas: MyCanvas) = canvas.update(field)

  def showNextState(state: Array[Array[Int]]):Unit = {
    display(state, cnvs)
    Thread sleep DELAY
    showNextState(getNextState(state))
  }

  def initialState() = Array.ofDim[Int](SIZE, SIZE)

  def getNextState(state: Array[Array[Int]]): Array[Array[Int]] = {
    val coordinates = (for (x <- 0 to SIZE - 1) yield {
      (for (y <- 0 to SIZE - 1) yield new Pointt(x, y)).toArray
    }).toArray
    coordinates.map(x => x.map(y => getStateForCoordinate(state, y.x, y.y)))
  }

  def getStateForCoordinate(state: Array[Array[Int]], x: Int, y: Int): Int = (state(x)(y), getSumForCoordinate(state, x, y)) match {
    case (1, 2 | 3) => 1
    case (0, 3) => 1
    case _ => 0
  }


  def getSumForCoordinate(state: Array[Array[Int]], x: Int, y: Int) = getNeighbours(state, x, y) reduceLeft {
    _ + _
  }

  /**
   * Get value of neighbours
   * @param state
   * @param x
   * @param y
   */
  def getNeighbours(state: Array[Array[Int]], x: Int, y: Int): Array[Int] =
    getNeighbourCoordinates(x, y)map(i => state(i.x)(i.y))


  def getNeighbourCoordinates(x: Int, y: Int): Array[Pointt] = (for {
    xx <- x - 1 to x + 1
    yy <- y - 1 to y + 1
    if (xx >= 0 && yy >= 0 && xx < (SIZE - 1) && yy < (SIZE - 1) && (x!=xx || y!=yy))
  } yield new Pointt(xx, yy)
    ).toArray
}
