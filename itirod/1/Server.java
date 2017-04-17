import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.net.DatagramSocket;
import java.net.DatagramPacket;
import java.net.InetAddress;

class Server
{
    public static DatagramSocket serverSocket;
    public static DatagramPacket datagramPacket;
    public static BufferedReader reader;
    public static InetAddress localHost;
    public static byte buffer[] = new byte[1024];
    public static int clientPort = 8080;
    public static int serverPort = 8081;
    
    public static void main(String[] a) throws IOException {
        serverSocket = new DatagramSocket(serverPort);
        datagramPacket = new DatagramPacket(buffer,buffer.length);
        reader = new BufferedReader(new InputStreamReader(System.in));
        localHost = InetAddress.getLocalHost();
        System.out.println("Server is Running...");
        while(true) {
            serverSocket.receive(datagramPacket);
            String clientString = new String(datagramPacket.getData(), 0, datagramPacket.getLength());
            if(clientString.equals("exit")) {
                System.out.println("Terminated...");
                break;
            }
            System.out.println("Client: " + clientString);
            String tempSting = new String(reader.readLine());
            buffer = tempSting.getBytes();
            serverSocket.send(new DatagramPacket(buffer, tempSting.length(), localHost, clientPort));
        }
    }
}
