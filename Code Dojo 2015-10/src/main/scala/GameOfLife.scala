import scala.swing._

object GameOfLife {
  def main(args: Array[String]) {
    var test = Seq(Seq(1, 2, 3), Seq(4, 5, 6), Seq(7, 8, 9))
    display(test)

    var frame = new MainFrame {
      visible = true
      title = "Game of Life"
    }
  }

  def display(field: Seq[Seq[Int]]) = {
    for (row <- field) {
      for (x <- row) {
        print(x)
      }
      println
    }
  }
}
