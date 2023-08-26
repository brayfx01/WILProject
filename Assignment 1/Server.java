
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.nio.Buffer;

import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;
import java.util.Collections;
import java.util.Comparator;
public class Server  {

    // this will calculate the tax payable by a client 
    public static String calculateTax(String tax, List<TaxRange> list)
    {
        float taxPayable = 0;

        // go through the list of tax ranges and find where tax lands
        for(TaxRange range : list)
        {
            // if we start in this range
            if(Integer.parseInt(tax) >= range.getStart() && Integer.parseInt(tax) <= range.getEnd())
            {
                // get the base tax 
                // getting the tax in the range
                taxPayable = taxPayable + (Float.parseFloat(tax) - range.getStart()) * (range.getTaxPerDollar())/100;
                // now adding in the base tax
                taxPayable = taxPayable + range.getBaseTax();
               
                // now return this as a string
                return Float.toString(taxPayable);
            }
        }
        return "I DON'T KNOW";
    }

    public static void taxTableHandler(List<TaxRange> list, TaxRange range)
    {

        int size = list.size();
        // will be used to determine if we are on the last range
        int currentRange = 0;
        // if this is false we do not add
        boolean add = false;
        // this will handle if two endpoints are the same or if there needs to be 
        // some shortening of the ranges

        // for each range in the list
        for(TaxRange obj: list)
        {

            // check if start and end are the same and the replace it with the newer one
            if(obj.getStart() == range.getStart() && obj.getEnd() == range.getEnd())
            {
                

                // replace this with the new one and exit the loop 
                obj.setBaseTax(range.getBaseTax());
                obj.setTaxPerDollar(range.getTaxPerDollar());
                add = false;
                break;
                // if our start range is smaller than the previous one
            }else if(obj.getStart() >= range.getStart() && obj.getEnd() <= range.getEnd())
            {

                // we replace obj with range
                obj.setStart(range.getStart());
                obj.setEnd(range.getEnd());
                obj.setBaseTax(range.getBaseTax());
                obj.setTaxPerDollar(range.getTaxPerDollar());
                add =false;
                currentRange += 1;
                continue;
            }
            // if we start in the range of one 
            else if(obj.getStart() <= range.getStart() && obj.getEnd() >= range.getEnd())
            {

                // we move the obj end to the ranges start
                obj.setEnd(range.getStart());
                //move the ranges start by 1 
                range.setStart(range.getStart() + 1);
                // now we continue to check if any other issues occure
                add = true;
                currentRange += 1;
                continue;
            // our new range starts in anouther and ends in anouther
            }else if(obj.getStart() <= range.getStart() && obj.getEnd()< range.getEnd())
            {
                // we set the end of the obj to the start of the rannge and increment the range by 1 
                obj.setEnd(range.getStart() -1);
                // incrementing the start of the range
                range.setStart(obj.getEnd() + 1);
                // now just continue why because this will conflict with anouther speciffically the end will be in anouther
                add = true;
                currentRange += 1;
                continue;
            }else if(obj.getStart()>= range.getStart() && obj.getStart() <= range.getEnd())
            {

                // set the start one more than the end of the range
                obj.setStart(range.getEnd() + 1);
                add = false;
                currentRange += 1;
                continue;
                // case we land in anouther with our end but not start
            }else if(obj.getStart() > range.getStart() && obj.getEnd() > range.getEnd() && obj.getStart() < range.getEnd())
            {

                // move the start of the obj to that of the end + 1
                obj.setStart(range.getEnd() + 1);
                add = true;
                currentRange += 1;
                continue;
                // if we added one that is far larger then all the ends of the others
            }else if(obj.getEnd() <= range.getStart())
            {
                // if we are on the last of the ranges then we can add it after 
                if(currentRange + 1 == size)
                {
                    // move the objects end to 1 below the new entry 
                    obj.setEnd(range.getStart() -1);
                    add = true;
                    continue;
                }
            //if the newly entered range is shorter than the privous ranges start
            }else if(obj.getStart() > range.getStart())
            {
                // move the older start to range start + 1
                obj.setStart(range.getEnd() + 1);
                add = true;
            }
      
        }
        // if none of the conditions apply then we can add to the list

        if (add == true)
            list.add(range);
        // now sorting the list
        // Create a custom Comparator to sort MyObject based on the 'value' field
        Comparator<TaxRange> comparator = Comparator.comparingInt(TaxRange::getStart);
        // Sort the ArrayList using the custom Comparator
        Collections.sort(list, comparator);


        

    }

    // will handle the updating function for the Server
    public static void Update(BufferedReader in, PrintWriter out,List<TaxRange> list)
    {
        // used to determine wether client entered start, end base ect 
        Integer num = 0;
        // these will be the start end bastTax and tax range 
        int start = 0;
        int end  = 0;
        int baseTax = 0;
        int taxPerDollar = 0;
        
        String msg = "";
        // getting the next message
        try {
            // get the string
            while(!msg.equals("~"))
            {
                 msg = in.readLine();
                // turn it into an integer
            
                if(!msg.equals("~"))
                {
                    Integer.parseInt(msg);
                }
                

               
                if(num == 0)
                {
                   start = Integer.parseInt(msg);
                }else if (num == 1)
                {
                    end = Integer.parseInt(msg);
                }else if(num == 2)
                {
                    baseTax = Integer.parseInt(msg);
                }else if(num == 3)
                {
                    taxPerDollar = Integer.parseInt(msg);
                }
                // determines how many msg sent to determine wether start, end ect
                num += 1;


            }


            // this will be used to ensure that tax raneges abide by the specified rule 
            // that being new entires replace or shorten or lengthen older ones
            
            // if the size of the list > there are possibilities of conflicts
            if(list.size() >= 1)
            {
                TaxRange range  = new TaxRange(start, end, baseTax, taxPerDollar);
                taxTableHandler(list, range);
            }else  // otherwise just add the new TaxRange object
            {

                TaxRange range = new TaxRange(start, end, baseTax, taxPerDollar);
                // add it to the list
                list.add(range);
            }

        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }

    }
    // will pint the tax range when asked
    public static void printTaxTable(BufferedReader in, PrintWriter out,List<TaxRange> list)
    {
        
        if(list.size() > 0)
        {
            for (TaxRange object: list)
            {

                out.println(object.getStart() + "-" + object.getEnd() + "  " + object.getBaseTax() + "  "+ object.getTaxPerDollar());
            }
        }
        out.println("QUERY: OK");

    }
    public static void main(String[] args)
    {
        // this is what will be used to store the tax ranges
        List<TaxRange> list = new ArrayList<>();

        System.out.println("Please choose your port number");
        Scanner scan = new Scanner(System.in);
        String portNumber = "";
        portNumber = scan.nextLine();
        
        try (
            //create a new serverSocket called ss
            
            ServerSocket serverSocket = new ServerSocket(Integer.parseInt(portNumber));
           
           
        ) {
          
                Socket clientSocket =  null;
                PrintWriter out = null;
                BufferedReader in = null;
                String msg = "";
                while(clientSocket == null)
                {
                    System.out.println("CONNECTION OPEN");
                    clientSocket = serverSocket.accept();

                    out = new PrintWriter(clientSocket.getOutputStream(), true);
                    //reads the incoming message from the client
                    in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
                    // writes to the socket
      
                    msg = in.readLine();
                    // if the client SENDS TAX ACCEPT
                    // if not then deny access
                    if(!msg.equals("TAX"))
                    {
                        out.println("DENIED");
                        clientSocket.close();
                        // set the clientSocket back to null waiting for the next client
                        clientSocket = null;

                    }else
                    {
                        // send back the message
                        System.out.format("CLIENT: %s\n", msg);
                        out.println("SERVER: " + msg +":" +" OK" );
                    }

                }
          

                // continue waiting for a connection untli close is done
                while (true) 
                    {
                        // checks if the client has disconnectd 
                        // if so waits for anouther
             
                        while(clientSocket.isClosed())
                        {
                            System.out.println("Waiting for next client");   
                            clientSocket = serverSocket.accept();

                            out = new PrintWriter(clientSocket.getOutputStream(), true);
                            in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));

                            // writes to the socket
                            System.out.println("CONNECTION OPEN");
                            msg = in.readLine();
                                    // send back the message
                            if(!msg.equals("TAX"))
                            {
                                out.println("DENIED");
                                clientSocket.close();
                            }else
                            {
                                System.out.format("CLIENT: %s\n", msg);
                                out.println("SERVER: " + msg +":" +" OK" );
                            }
                            

                        }
                        // get the next in line
                        System.out.println("Waiting for next string");
                        msg = in.readLine();
                        System.out.println("CLIENT: " + msg);
                        // will only accept client if they ask for tax
                        //System.out.println("START " + msg);
                        if(clientSocket.isClosed())
                        {
                            System.out.println("Waiting for new socket");
                        }

                        if (msg.equals("TAX")) {
                            //accept an client socket


                            // send back this message
                            out.println("SERVER: " + msg +":" + " OK" );

                        }
                        // dealing with the UPDATE functionality
                        else if(msg.equals("UPDATE"))
                        {

                            
                            Update(in,out,list);
                            out.println("SERVER: UPDATE: OK");



                        } else if(msg.equals("QUERY"))
                        {
                    
                            out.println("SERVER: ");
                            printTaxTable(in,out ,list);
                        // if the msg sent is all numbers then 
                        // the client is requesting to calculate their taxes
                        }else if(msg.matches("\\d+") || msg.matches("-?\\d+(\\.\\d+)?") )
                        {
                            String tax = "";
                            // calculate what the client is expected to pay in tax
                            tax = calculateTax(msg,list);
                            // return the tax payable
                            // sees if tax matches either a integer or a float
                            if(tax.matches("\\d+") || tax.matches("-?\\d+(\\.\\d+)?"))
                            {
                                out.println("SERVER: TAX PAYABLE IS " + tax);
                            }else
                            {
                                out.println("SERVER: WE DON't KNOW " + msg);
                            }
                        
                        }
                        else if(msg.equals("CLOSE"))
                        {
                            out.println("Server: CLOSE: OK");
                            // close both sockets
                            clientSocket.close();
                            serverSocket.close();
                            // This brevents any futher reading of the socket when closed
                            break;
                        }else if (msg.equals("BYE"))
                        {
                            out.println("SERVER: BYE: OK");
                            //close th client socket
                            clientSocket.close();
                          
                            continue;
                        }
                        // else print unknown command
                        else {
                            out.println("UNKNOWN COMMAND" + msg );
        
                        
                        }
              
                    }
         
        } catch (IOException e) {
            System.err.println("Error in server: " + e.getMessage());
            e.printStackTrace();
            scan.close();
        }
    }
}



