import java.nio.charset.Charset;
import java.math.BigInteger;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.BufferedOutputStream;
import java.io.FileReader;
import java.io.File;
import java.io.InputStream;
import java.awt.*;
import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;

class Steganography {
    public static void main(String [] args) throws Exception {
        ImageProcess imp = new ImageProcess("2.png", "new2.png", "input.txt");
        imp.hide();
        imp.reveal();
    }
}

class ImageProcess{
    private String inputImageName;
    private String outputImageName;
    private String inputTextName;
    private BufferedImage inputImage;
    private byte[] text;

    ImageProcess() {}

    ImageProcess(String inputImageName, String outputImageName, String inputTextName) {
        this.inputImageName = inputImageName;
        this.outputImageName = outputImageName;
        this.inputTextName = inputTextName;
    }

    public void readInputTextFile() throws Exception {
        FileReader file = new FileReader(inputTextName);
	BufferedReader in = new BufferedReader(file);
	String s = "";
	String text = "";
	while((s=in.readLine())!=null) {
	    text = text + s + "\n";
        }
        this.text = txtToByte(text);
    }

    private byte[] txtToByte(String s) {
	byte [] arr = s.getBytes(Charset.forName("UTF-8"));
	return arr;
    }

    public BufferedImage fetchImage(String name) throws Exception {
	File f = new File(name);
	BufferedImage img = ImageIO.read(f);
	return img;
    }

    public void hideText(BufferedImage img , byte [] txt) throws Exception {	
	int i = 0;
	int j = 0;
	for(byte b : txt){
	    for(int k=7;k>=0;k--){
		Color c = new Color(img.getRGB(j,i));
		byte blue = (byte)c.getBlue();
		int red = c.getRed();
		int green = c.getGreen();
		int bitVal = (b >>> k) & 1;  
		blue = (byte)((blue & 0xFE)| bitVal);
		Color newColor = new Color(red,
		green,(blue & 0xFF));
		img.setRGB(j,i,newColor.getRGB());
		j++;
            }
	    i++;
	}
	
	createImgWithMsg(img);
	System.out.println("Text Hidden");
    }
	
    public void createImgWithMsg(BufferedImage img) {
	try {
	    File ouptut = new File("new2.png");
	    ImageIO.write(img, "png", ouptut);
	}
	catch(Exception ex) {}
    }

    public void hide() throws Exception {
        readInputTextFile();
        inputImage = fetchImage(inputImageName);
        hideText(inputImage, text);
    }

    public String revealMsg(String fileName, int msgLen) throws Exception {
        BufferedImage img = fetchImage(fileName);
	byte [] msgBytes = extractHiddenBytes(img,msgLen);
	if(msgBytes == null) {
            return null;
        }
        String msg = new String(msgBytes);
	return (msg);
    }
	
    public byte[] extractHiddenBytes(BufferedImage img , int size) {	
        int i = 0;
        int j = 0;
        byte [] hiddenBytes = new byte[size];

	for(int l=0;l<size;l++){
	    for(int k=0 ; k<8 ; k++){
		Color c = new Color(img.getRGB(j,i));
		byte blue = (byte)c.getBlue();
		int red = c.getRed();
		int green = c.getGreen();
		hiddenBytes[l] = (byte) ((hiddenBytes[l]<<1)|(blue&1));
		j++;
	    }
	    i++;
	}
	return hiddenBytes;	
    }

    public void reveal() throws Exception {
        System.out.println("Message in image:");
        System.out.println(revealMsg(outputImageName, text.length));
    }
}
