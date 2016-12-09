/**
 * Created by ss7n13 on 10/07/15.
 */
object GameStateFactory {
  val arr_blinker = Array(
    "_x_",
    "_x_",
    "_x_"
  )
  def blinker(state: Array[Array[Int]], x: Int, y: Int) = makeState(state, arr_blinker, x, y)

  def makeState(state: Array[Array[Int]], config: Array[String], x: Int, y: Int) = {
    var x = 0
    var y = 0
    def trans = Seq()
    for (row <- config) {
      for (c <- row) {
        x += 1
        if (c == 'x') trans:+(x, y)
      }
      x = 0
      y += 1
    }
    trans.foreach(pt => {
      state(pt._0 + x, pt(1) + y) = 1
    })
  }
}
