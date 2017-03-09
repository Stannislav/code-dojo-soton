var config = Array(
  "_x_",
  "_x_",
  "_x_"
)
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
println(trans)