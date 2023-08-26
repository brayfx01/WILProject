import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.Scanner; 
public class test 
{


    public static void main(String[] args) 
    {
        Update();
    }

    
      // Will hold the update functionality for the client
    public static void Update()
      {
          Scanner scan = new Scanner(System.in);
          int start;
          int end;
          int baseTax;
          int taxPerDollar;
          // going and getting user inputfor each of the reqruied parameters for tax range
          System.out.println("Please insert the Start Range income");
          start = scan.nextInt();
          System.out.println("Please Insert the End Rnage Income");
          end = scan.nextInt();
          System.out.println();
          System.out.println("Please insert the base Tax rate for the income range");
          baseTax = scan.nextInt();
          System.out.println("Please insert the tax(in cents) per dollar");
          taxPerDollar = scan.nextInt();
          
          System.out.println("THESE ARE WHAT YOU HAVE");
          System.out.println(start);
          System.out.println(end);
          System.out.println(baseTax);
          System.out.println(taxPerDollar);
          scan.close();
  
      }
}
