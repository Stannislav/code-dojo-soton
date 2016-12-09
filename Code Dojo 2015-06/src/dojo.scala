/**
 * Created by ss7n13 on 15/06/15.
 */
import java.awt.{Color, FlowLayout, Graphics2D}
import java.awt.image.BufferedImage
import java.io.File
import javax.imageio.ImageIO
import javax.swing.{ImageIcon, JLabel, JFrame}

object Evolve {
  def main(args: Array[String]): Unit = {
    var img = ImageIO.read(new File("/Users/ss7n13/Desktop/img.jpg"))
    var blackWhite = new BufferedImage(img.getWidth(), img.getHeight(), BufferedImage.TYPE_BYTE_BINARY)
    var g2d:Graphics2D = blackWhite.createGraphics()
    g2d.drawImage(img,0,0,null)
    g2d.dispose()
    img = blackWhite

    var i = new ImageIcon(img.getScaledInstance(200, 200,  java.awt.Image.SCALE_FAST))
    var i2 = new ImageIcon(img.getScaledInstance(200, 200,  java.awt.Image.SCALE_FAST))
    var bestScore = new JLabel("")
    var iIcon = new JLabel(i)

    var frame = new JFrame()
    frame.getContentPane().setLayout(new FlowLayout())
    frame.getContentPane().add(iIcon)
    frame.getContentPane().add(new JLabel(i2))
    frame.getContentPane().add(bestScore)
    frame.pack()
    frame.setVisible(true)

    println("Generating population.")
    var population = this.generatePopulation(img.getWidth, img.getHeight, 10)

    println("Sorting population.")
    population = population sortBy {fitness(_, img)}

    var x = 0
    println("Starting loop.")
    while (true) {
      x += 1
      println(x)
      population = evolve(population, img)
      bestScore.setText(x.toString() + " " + fitness(population.head, img).toString())
      i.setImage(population.head.getScaledInstance(200, 200,  java.awt.Image.SCALE_FAST))
      iIcon.repaint()
    }

  }

  //  def evolve(population: IndexedSeq[BufferedImage], originalImage:BufferedImage): IndexedSeq[BufferedImage] = {
  //    var to_breed = for (x <- population.take(10); y <- population.take(10)) yield (x, y);
  //
  //    var t = to_breed.map {case (x:BufferedImage, y:BufferedImage) => breed(x, y)}
  //    return t sortBy (x => fitness(x, originalImage));
  //  }

  def evolve(population: IndexedSeq[BufferedImage], originalImage:BufferedImage): IndexedSeq[BufferedImage] = {
    var to_breed = for (x <- population.take(10); y <- population.take(10)) yield (x, y);

    var t = to_breed.flatMap {case (x, y) => List(breed(x, y), breed(x, y), breed(x, y), breed(x, y),breed(x, y),breed(x, y),breed(x, y),breed(x, y),breed(x, y),breed(x, y))}
    return t sortBy (x => fitness(x, originalImage));
  }

  def breed(a: BufferedImage, b:BufferedImage): BufferedImage = {
    println("Breeding.")
    var newImg = new BufferedImage(a.getWidth, a.getHeight, BufferedImage.TYPE_BYTE_BINARY);
    var r = new scala.util.Random(System.currentTimeMillis);
    (0 until a.getWidth).foreach(x =>
      (0 until a.getHeight).foreach(y => {
        val rr = r.nextInt(6);
        val nextVal = if (rr < 3) a.getRGB(x, y) else if (rr < 5) b.getRGB(x, y) else if (r.nextBoolean()) Color.WHITE.getRGB() else Color.BLACK.getRGB()
        newImg.setRGB(x, y, nextVal)
      })
    )
    return newImg;
  }

  def generatePopulation(width:Int, height:Int, n:Int): IndexedSeq[BufferedImage] = (0 until n).map(x => this.generateImage(width, height))

  def generateImage(width: Int, height: Int): BufferedImage = {
    var b = new BufferedImage(width, height, BufferedImage.TYPE_BYTE_BINARY);
    var r = new scala.util.Random(System.currentTimeMillis);
    (0 until width).foreach(x =>
      (0 until height).foreach(y => {
        b.setRGB(x, y, if (r.nextBoolean()) Color.WHITE.getRGB() else Color.BLACK.getRGB())}
      )
    )
    return b;
  }

  def fitness(a: BufferedImage, b: BufferedImage): Int = {
    println("Computing fitness.")
    var p = for (x <- 0 until a.getWidth; y <- 0 until a.getHeight) yield (x, y)
    var all_weights = p.map {case (x, y) => if (a.getRGB(x, y) == b.getRGB(x, y)) 0 else 1}
    return all_weights.sum
  }
}
