var k = Array(1, 2, 3)
def test(arr: Array[Int]) = {
  arr(1) += 3
  arr
}
test(k)
k foreach(println(_))
