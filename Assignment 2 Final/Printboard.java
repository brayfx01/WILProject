import java.security.cert.TrustAnchor;

import javax.print.FlavorException;

public class Printboard
{
    public static void  Print(Cell[][] board, int row, int column) 
    {
      
        
  
        
       
        String greenColor = "\u001B[32m";
        String resetColor = "\u001B[0m"; // Reset to default color
        String blueColor = "\u001B[34m";
        String redColor = "\u001B[31m";
        // this is for the bottom frow specifically to stop double printing +--
        Boolean previousTrue = false;

        // going through and printing the board 
        for (int i = 0; i < row; i++)
        {
            
            System.out.print("  ");
            if(i != 0)
            {
                //print the top of grid 
                for (int k = 0; k < row; k++)
                {
                    
                    //print the number 
                    if(k + 1 != row)
                    {
                        // if there is a ship colour this green
                        // or if the previous square had a ship
                        if(board[i][k].containsShip == true )
                        {

                            System.out.print(  greenColor + "s--");
                            // resets the colour so the rest of the board does not go green
                            System.out.print(resetColor);
                        //previous spot had a ship
                        }else if(board[i][k].left == true && board[i][k-1].containsShip == true )
                        {
                            // we just want the s to be green
                            System.out.print(  greenColor + "s" + resetColor + "--" );
                        
                        //cell above has a ship
                        }else if(board[i][k].up == true && board[i-1][k].containsShip == true)
                        {
                            //green and reset
                            System.out.print(  greenColor + "s--");
                            System.out.print(resetColor);
                        // both up and left are true
                        }else if(board[i][k].left == true && board[i][k].up == true && board[i-1][k-1].containsShip == true )
                        {
                             System.out.print( greenColor + "s" + resetColor +  "--");
                        }
                        else
                        {
                            System.out.print( "+--");
                        }
                    }else//ending row so do this instead
                    {
                         // if there is a ship colour this green
                        if(board[i][k].containsShip == true)
                        {
                            System.out.print(  greenColor + "+--+");
                            // resets the colour so the rest of the board does not go green
                            System.out.print(resetColor);
                        // the above cell had a ship
                        } else if(board[i][k].up == true && board[i-1][k].containsShip == true)
                        {
                            System.out.print(  greenColor + "+--+");
                            // resets the colour so the rest of the board does not go green
                            System.out.print(resetColor);
                        } else if(board[i][k].left == true && board[i][k].up == true && board[i-1][k-1].containsShip == true )
                        {
                            System.out.print( greenColor + "s" + resetColor + "--+");
                        //top rigth corner of the grid
                        }
                        else if( board[i][k].left == true && board[i][k-1].containsShip == true)
                        {
                            System.out.print( greenColor + "s" + resetColor + "--+");
                        }
                        else
                        {
                            System.out.print( "+--+");
                        }
                       
                    }
                }
                //print the walls and letter
                System.out.println("");
                // print the row letter
                char rowLetter = AlphabetArray.convertNumberToString(i);
                System.out.print(rowLetter + " ");

               
                for (int k = 0; k < column; k++)
                {
                    //print the number 
                    if(k+1 != column)
                    {
                        if(board[i][k].containsShip == true)
                        {
                            char character = board[i][k].shipName.charAt(0);
                            System.out.print( greenColor +"|" + character + " ");
                            System.out.print(resetColor);
                        //previous cell ahs ship
                        }else if(board[i][k].left == true && board[i][k-1].containsShip == true)
                        {
                            System.out.print( greenColor +"|" + " " + " ");
                            System.out.print(resetColor);
                        }
                        // hit and miss functionality
                        else if(board[i][k].miss == true)
                        {
                            System.out.print( blueColor +"|" + "O" + " ");
                            System.out.print(resetColor);
                        }else if(board[i][k].hit == true)
                        {
                            System.out.print( redColor +"|" + "X" + " ");
                            System.out.print(resetColor);
                        }
                        else
                        {
                            System.out.print( "|  ");
                        }
                       
                    }else
                    {
                        if(board[i][k].containsShip == true)
                        {
                            char character = board[i][k].shipName.charAt(0);
                            System.out.print( greenColor +"|" + character + " " + "|");
                            System.out.print(resetColor);
                        }else if(board[i][k].miss == true)
                        {
                            System.out.print( blueColor +"|" + "O" + " " + "|");
                            System.out.print(resetColor);
                        }else if(board[i][k].hit == true)
                        {
                            System.out.print( redColor +"|" + "X" + "|");
                            System.out.print(resetColor);
                        }
                        // turning it green 
                        else if(board[i][k].left == true && board[i][k-1].containsShip == true)
                        {
                            System.out.print(greenColor + "|" + resetColor + "  |");
                        }
                        else
                        {
                            System.out.print("|  |");
                        }
                     
                    }
                  
                }
                System.out.println("");
                
            }else //pritn the column numbers
            {
                System.out.print(" ");
                for (int k = 0; k < row; k++)
                {
                    //print the number 
                    if(k < 9)
                        System.out.print((k+1) + "  ");
                    else
                         System.out.print((k+1) + " " );
                }
                //move to the next row
                System.out.println();
                //spacing
                System.out.print("  ");
                for(int k = 0; k < column; k++)
                {
                   
                     //print the number 
                    if(k + 1 != row)
                    {
                    
                        // if there is a ship colour this green
                        if(board[i][k].containsShip == true)
                        {
                            System.out.print(  greenColor + "s--");
                            // resets the colour so the rest of the board does not go green
                            System.out.print(resetColor);
                        }else if(board[i][k].left == true && board[i][k-1].containsShip == true)
                        {
                            System.out.print(  greenColor + "s" + resetColor + "--");
                        }
                        else
                        {
                            System.out.print( "+--");
                        }
                    }else
                    {
                        if(board[i][k].left == true && board[i][k-1].containsShip == true)
                            System.out.print(greenColor + "s" + resetColor + "--+");
      
                        else
                            System.out.print("+--+");
                    }
                }
                
              
                //print the walls and letter
                System.out.println("");
                // print the row letter
                char rowLetter = AlphabetArray.convertNumberToString(i);
                System.out.print(rowLetter + " ");
                for (int k = 0; k < column; k++)
                {
         
                    if(k+1 != column)
                    {
                        if(board[i][k].containsShip == true)
                        {

                            char character = board[i][k].shipName.charAt(0);
                            System.out.print( greenColor + "|" + character + " ");
                            System.out.print(resetColor);
                        }else if(board[i][k].left == true && board[i][k-1].containsShip == true)
                        {
                             System.out.print( greenColor + "|" + " " + " ");
                            System.out.print(resetColor);
                        }
                        else if(board[i][k].miss == true)
                        {
                            System.out.print( blueColor + "|" + "O" + " ");
                            System.out.print(resetColor);
                        } else if(board[i][k].hit == true)
                        {
                            System.out.print( redColor +"|" + "X" + " ");
                            System.out.print(resetColor);
                        }
                        else
                        {
                            System.out.print( "|  ");
                        }
                       
                    }else
                    {
                        //oponents board does not contain any ship so skips this immediately
                        if(board[i][k].containsShip == true)
                        {
                            char character = board[i][k].shipName.charAt(0);
                            System.out.print( greenColor +"|" + character + " " + "|");
                            System.out.print(resetColor);
                        }else if(board[i][k].left == true && board[i][k-1].containsShip == true)
                        {
                              System.out.print(greenColor + "|" +resetColor + "  |");
                        }
                        else if(board[i][k].miss == true)
                        {
                            System.out.print( blueColor +"|" + "0" + " " + "|");
                            System.out.print(resetColor);
                        } else if(board[i][k].hit == true)
                        {
                            System.out.print( redColor +"|" + "X" + "|");
                            System.out.print(resetColor);
                        }
                        else
                        {
                            System.out.print("|  |");
                        }
                    }
                  
                }
                System.out.println("");

            }
    
           
      
        }
        // bottom grid
        
            System.out.print("  ");
            for(int k =0; k< column; k++)
            {
                 //print the number 
                    if(k+1  != column)
                    {
                        //minus one to fit into the array 
                        // if there is a ship colour this green
                        if(board[row - 1][k].containsShip == true)
                        {
                            System.out.print(  greenColor + "s--");
                            // resets the colour so the rest of the board does not go green
                            System.out.print(resetColor);
                        } 
                        else
                        {
                            if(board[row-1][k].left == true && board[row - 1][k -1].containsShip == true)
                            {
                                if(k+2 != column)
                                    System.out.print( greenColor+ "s" + resetColor + "--+");
                                else
                                {
                                    System.out.print( greenColor+ "s" + resetColor + "--");
                                }
                                previousTrue = true;
                                
                            }else //bottom row wich canges if the if was done prior
                            {
                                if(previousTrue == true)
                                {
                                     System.out.print("--");
                                     previousTrue = false;
                                }else
                                {
                                    System.out.print("+--");
                                }
                               
                            }
                            
                        }
                    }
                    // bottom right of the grid
                    if(k +1 == column)
                    {
                        System.out.print("+--+");
                    }
            }
            
        
      
    }
}
