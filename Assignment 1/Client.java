import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.Scanner; 

public class Client {

    // Will hold the update functionality for the client
    public static void Update(PrintWriter out, BufferedReader in)
    {
        Scanner scan = new Scanner(System.in);
        int start;
        int end;
        int baseTax;
        int taxPerDollar;

        // going and getting user inputfor each of the reqruied parameters for tax range
        System.out.println("Please insert the Start Range income");
        start = Integer.parseInt(scan.nextLine());
        // send this to the server 
        out.println(start);
        
        System.out.println("Please Insert the End Rnage Income");

        end = Integer.parseInt((scan.nextLine()));
        out.println(end);

        System.out.println("Please insert the base Tax rate for the income range");
        baseTax = Integer.parseInt((scan.nextLine()));
        out.println(baseTax);

        System.out.println("Please insert the tax(in cents) per dollar");
        taxPerDollar = Integer.parseInt((scan.nextLine()));
        out.println(taxPerDollar);
        //This marks the end of the update for the server
        out.println("~");



    }
    public static void main(String[] args) 
    {
        // geting the user input for the port 5000
        System.out.println("Please choose your port number");
        Scanner scan = new Scanner(System.in);
        String portNumber = "";
        portNumber = scan.nextLine();
        try (
           
            
           
            Socket socket = new Socket("127.0.0.1", Integer.parseInt(portNumber));
            BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
            
        ) {

            String command = "";
            String response = "";
            boolean skip = false;
            // this will loop back so the client can continue issiuing 
            //comands utnile BYE OR CLOSE IT DONE 
            // CLOSE IS A SPCEIAL case that will close both client and server sockets
            out.println("TAX");
            response = in.readLine();
            System.out.println(response);
            if(response.equals("DENIED"))
            {
                  
                System.exit(0);
            }
          
            while(!command.equals(("BYE")) && !command.equals("CLOSE"))
            {
         
                System.out.println("ENTER COMMAND");

                command = scan.nextLine();
                out.println(command);
                // send over the input
                if(command.equals("UPDATE"))
                {

                    
                    // testing with a number
                    System.out.println("BEFORE ENTERING NUMBER");

                   
                    // go to the update function
                    Update(out,in);
                    // get the response from the server
                // wait until we recive QUERY : OK by server
                }else if(command.equals("QUERY"))
                {
                    // server
                    response = in.readLine();
                    System.out.print(response);

                    response = in.readLine();
                    System.out.print(response + "\n");
                    while(true)
                    {
                        if(!response.equals("QUERY: OK"))
                        {
                            response = in.readLine();
                        }else
                        {
                            skip = true;
                            break;
                        }
                       
                        // if we receive this then break
                        if(response.equals("QUERY: OK"))
                        {
                            System.out.println(response);
                            command = "";
                            // skip the response at the end of this section
                            skip = true;
                            break;
                        }else 
                        {
                           
                            System.out.println("        " + response);
                        }
                    }
                           
                    
                }
                //pushing this command to the server
                if(skip == false)
                {
                    response = in.readLine();
                    System.out.println(response);
                }else 
                {
                    skip = false;
                }
        
                
            }  
            socket.close();
        } catch (IOException e) {
            System.err.println("Error in client: " + e.getMessage());
            e.printStackTrace();
        }

       

    }
    
}
