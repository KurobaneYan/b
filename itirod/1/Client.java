import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.DatagramSocket;
import java.net.DatagramPacket;
import java.net.InetAddress;

class Client
{
    public static DatagramSocket clientSocket;
    public static DatagramPacket datagramPacket;
    public static BufferedReader reader;
    public static InetAddress localHost;
    public static byte buffer[] = new byte[1024];
    public static int clientPort = 8080;
    public static int serverPort = 8081;

    public static void main(String[] a) throws IOException {
        clientSocket = new DatagramSocket(clientPort);
        datagramPacket = new DatagramPacket(buffer, buffer.length);
        reader = new BufferedReader(new InputStreamReader(System.in));
        localHost = InetAddress.getLocalHost();
        System.out.println("Client is Running... Type 'STOP' to Quit");
        while(true) {
            String tempString = new String(reader.readLine());
            buffer = tempString.getBytes();
            if(tempString.equals("exit")) {
                System.out.println("Terminated...");
                clientSocket.send(new DatagramPacket(buffer, tempString.length(), localHost, serverPort));
                break;
            }
            clientSocket.send(new DatagramPacket(buffer, tempString.length(), localHost, serverPort));
            clientSocket.receive(datagramPacket);
            String serverString = new String(datagramPacket.getData(), 0, datagramPacket.getLength());
            System.out.println("Server: " + serverString);
        }
    }
}
