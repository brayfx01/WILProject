import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.*;
import java.util.Random;
import java.util.Scanner;
import java.util.regex.*;


public class playerOne {

    public static Scanner scanner = new Scanner(System.in);
    static String playerName = "";

        
    public static String[] sunkenShip  = new String[5];


    public static boolean gameOver = false;
    public static boolean currentTurn = false;
    public static boolean won = true;
    public static boolean alreadySunk = false;
       // these are what the row and column player chosses
    public static int gridSize = 0;
    public static int gridRowSize =0;
    public static int gridColumnSize =0;
    public static int firedRow = 0;
    public static int firedColumn =0;
    public static int totalShip = 5; // we have a total of 5 shps
    public static int tcpPort = 0;
    // place the battelships
    public static void fireOperation(BufferedReader reader, PrintWriter writer,int gridRow, int gridColumn) 
    {
        // Prompt the user for input
        System.out.print("Enter Grid Coordinace e.g: FIRE: A-3 ");
  
        // Read a line of text entered by the user
        String userInput = scanner.nextLine();
         // Define a regular expression pattern
        String pattern = "FIRE:[A-Z]-\\d+";
        // Create a Pattern object
        Pattern regexPattern = Pattern.compile(pattern);

        // Match the input against the pattern
        Matcher matcher = regexPattern.matcher(userInput);
        System.out.println(matcher.matches());

        while(!matcher.matches())
        {
          
                System.out.println("");
                System.out.print(userInput + " Invalid input, please enter cordinates of the form FIRE:A-3:");
                userInput = scanner.nextLine();
                matcher = regexPattern.matcher(userInput);
        }
  

        // Split the input string by ":" to separate "FIRE" and " A-3"
        String[] parts = userInput.split(":");

        String secondPart = "";
        String firstPart = "";
      
        
        while(true)
        {
            if (parts.length == 2) {
                firstPart = parts[0].trim();
                secondPart = parts[1].trim();
            }

            // Extract "A" and "3" from the second part
            String[] subParts = secondPart.split("-");
            String letter = "";
            String number = "";
        
            if (subParts.length == 2) {
                letter = subParts[0].trim();
                number = subParts[1].trim();
            

            }
        
            int row = 0;
            int column = 0;
        
            row = AlphabetArray.convertLetterToNumber(letter);
         
            
            column = Integer.valueOf(number);

            firedRow  = row;
            firedColumn = column;

            // tihs means we are in the board boundaries
            if(row > 0 && row <= gridRow && column > 0 && column <= gridColumn)
            {
                 // now we send and wait for a response 
                writer.println(row);
                writer.println(column);
                break;
            }else
            { // if we are out of bounds
                System.out.println("cordinates are out of bounds please try again board size is (" + gridRowSize + "," + gridColumnSize + ")");
                userInput = scanner.nextLine();
                matcher = regexPattern.matcher(userInput);
                //checks to make sure it is in the right format
                while(!matcher.matches())
                {
                
                        System.out.println("");
                        System.out.print(userInput + " Invalid input, please enter cordinates of the form FIRE:A-3:");
                        userInput = scanner.nextLine();
                        matcher = regexPattern.matcher(userInput);
                }

                   if (parts.length == 2) 
                    {
                        firstPart = parts[0].trim();
                        secondPart = parts[1].trim();
                    }
                    parts = userInput.split(":");
                    // Extract "A" and "3" from the second part
                    subParts = secondPart.split("-");
                    letter = "";
                    number = "";
                        
                    if (subParts.length == 2) {
                        letter = subParts[0].trim();
                        number = subParts[1].trim();
                    

                    }
        
                
            }


        }
       

    }

    public static void placeBattleShips(int[] shiplength, String[] shipNames, Cell[][] board, int rows, int columns) {
        // we are going to randomly choose a position and if it is not suitable add it
        // to this list
        // both need to be synced ie row[0]column[0] gives us the cell
        int[] rowPositionChecked = new int[rows];
        int[] columnPositionChecked = new int[columns];
        // determines when we place a ship
        boolean placed = false;

        Random random = new Random();
        int randomRow = random.nextInt(rows);
        int randomColumn = random.nextInt(columns);

        // now doing the cheking
        // how many more cells we need for the ship
        // 0 is first 4 is fifth
        int currentShip = 0;
        // minus one is for the start row and column
        int lengthOfShip = shiplength[currentShip] - 1;
        int currentlengthofShip = lengthOfShip;

        // does this cell already have a ship if not then we can continue
        // checking more cells and recording them to place them

        int startRow = randomRow;
        int startColumn = randomColumn;
        // for the current row and column we are on
        int currentRow = startRow;
        int currentColumn = startColumn;
        // recording the rows and columns as to place the boat after confirming that
        // it can fit
        int[] rowRecord = new int[rows];
        int[] columnRecord = new int[columns];
        
        // this will prevent moving donw then up or left then down ect
        int currentDirection = 0; // 0 for up 1 for right 2 for down 3 for left



       
        while (placed == false) {


            if (board[currentRow][currentColumn].containsShip == false && currentlengthofShip > 0) {
         

   
                // subtract 1 from the length of ship
                // for recording the available rows and columns though should only be
                // max of the boat size to place
                if (currentDirection == 4) {

                    // choosing new starting spot
                    randomRow = random.nextInt(rows);
                    randomColumn = random.nextInt(columns);
                    // reseting everything
                    startRow = randomRow;
                    startColumn = randomColumn;

                    currentRow = startRow;
                    currentColumn = startColumn;

                    currentlengthofShip = lengthOfShip;

                    currentDirection = 0;

                }
                // can we move up
                if (board[currentRow][currentColumn].up == true && currentDirection == 0) {
              
                    currentlengthofShip -= 1;
                  
                    // lengthOfShip - currentlengthofShip)-1
                    // the above calculates how many we have placed minusing the 1 from the random
                    // point

                    rowRecord[(lengthOfShip - currentlengthofShip) - 1] = currentRow - 1;
                

                    // bassiaclly finding the diffeerence to determine how many cells
                    // we have previously recorded

                    columnRecord[(lengthOfShip - currentlengthofShip) - 1] = currentColumn;
                   
                    // now settign the new row to be checked again
                    currentRow = currentRow - 1;
                    // go back up and check the next up row
                    continue;

                } else if (currentDirection == 0) // we cannot continue going up so switch directions
                {

                    currentRow = startRow;
                   
                    currentDirection = 1;
                    currentlengthofShip = lengthOfShip;
                  
                    continue;
                }

                // can we move right
                if (board[currentRow][currentColumn].right == true && currentDirection == 1) {
        
                    currentlengthofShip -= 1;

                    columnRecord[(lengthOfShip - currentlengthofShip) - 1] = currentColumn + 1;

           

                    rowRecord[(lengthOfShip - currentlengthofShip) - 1] = currentRow;

                    // now settign the new row to be checked again
                    currentColumn = currentColumn + 1;
                    // go back up and check the next up row
                    continue;
                } else if (currentDirection == 1)// switch to checking bottom direction
                {
                    currentColumn = startColumn;
                    currentDirection = 2;
                    currentlengthofShip = lengthOfShip;
                    continue;
                }
         
                // can we move down
                if (board[currentRow][currentColumn].down == true && currentDirection == 2) {
                  
           
                    currentlengthofShip -= 1;
             
                    rowRecord[(lengthOfShip - currentlengthofShip) - 1] = currentRow + 1; // moving up by one row
                  
                    // probably can do the same for the for above
                    columnRecord[(lengthOfShip - currentlengthofShip) - 1] = currentColumn;
                    // now settign the new row to be checked again
                    currentRow = currentRow + 1;
                    // go back up and check the next up row
                    continue;
                } else if (currentDirection == 2)// switch to checking bottom direction
                {
                    currentRow = startRow;
                    currentDirection = 3;// left direction now
                    currentlengthofShip = lengthOfShip;
                    continue;
                }

                // can we move left
                if (board[currentRow][currentColumn].left == true && currentDirection == 3) {
                    
               
                    currentlengthofShip -= 1;
                    columnRecord[(lengthOfShip - currentlengthofShip) - 1] = currentColumn - 1;

                    // update the column to be the same column as we moved rows
                    rowRecord[(lengthOfShip - currentlengthofShip) - 1] = currentRow;

                    // now settign the new row to be checked again
                    currentColumn = currentColumn - 1;
                    // go back up and check the next up row
                    continue;
                } else// switch to checking bottom direction
                {
                    currentRow = startRow;
                    currentDirection = 4;// left direction now
                    currentlengthofShip = lengthOfShip;
                }

            } else if (currentlengthofShip == 0 && board[currentRow][currentColumn].containsShip == false) {
                // this is where we will be doing the changing to other ship


                // now we want to go and set the cells we have found to contain a ship

                // set the starting cell to contain the ship
                board[startRow][startColumn].containsShip = true;
                board[startRow][startColumn].shipName = shipNames[currentShip];
                board[startRow][startColumn].shiplength = shiplength[currentShip];
             
                // now setting the rest of the cells
                for (int i = 0; i < lengthOfShip; i++) 
                {
                
              
                    board[rowRecord[i]][columnRecord[i]].containsShip = true;
                 
                    board[rowRecord[i]][columnRecord[i]].shipName = shipNames[currentShip];
           
                    board[rowRecord[i]][columnRecord[i]].shiplength = shiplength[currentShip];
                }
          
                if (currentShip < 4) {
                    currentShip += 1;
                } else {
              
                    placed = true;
                }

                lengthOfShip = shiplength[currentShip] - 1;
                currentlengthofShip = lengthOfShip;
                // picking two more reandom points
                randomRow = random.nextInt(rows);
                randomColumn = random.nextInt(columns);

                startRow = randomRow;
                startColumn = randomColumn;

                currentRow = startRow;
                currentColumn = startColumn;
                currentDirection = 0;


            } else {
              
                // if we detect a collision it is one of two things
             
                // the start cell is occupied
                // so change it and start again
                if (currentRow == startRow && currentColumn == startColumn) {
             
                    randomRow = random.nextInt(rows);
                    randomColumn = random.nextInt(columns);

                    startRow = randomRow;
                    startColumn = randomColumn;

                    currentRow = startRow;
                    currentColumn = startColumn;
                } else// we have collided while moving so change direction
                {
                    currentDirection += 1;
                    // set the ship length back to the origingal
                    currentlengthofShip = lengthOfShip;
                    // set the current row and column back to the start
                    currentRow = startRow;
                    currentColumn = startColumn;
                  
                }

            }
        }

    }
   
    public static Cell[][] createGrid(int rows, int columns, int operation) {

        // Create a 2D array (grid) with the specified dimensions
        Cell[][] board = new Cell[rows][columns];

        
        // populate the array with cells
        for (int i = 0; i < rows; i++) {

            for (int j = 0; j < columns; j++) {

                board[i][j] = new Cell();
               
                // cannot move up
                if (i == 0) {
                    board[i][j].up = false;
                   
                }
                // cannot move down
                if (i == rows - 1) {
                    board[i][j].down = false;
                  
                }
                // cannot move left
                if (j == 0) {
                    board[i][j].left = false;
                   
                }
                // cannot move right
                if (j == columns - 1) {
                    board[i][j].right = false;
                    
                }
            }
        }
        // if playerTWo board then we do not populate it with ships
        if(operation == 1)
        {
            System.out.println("Opponents Board");
            Printboard.Print(board, rows, columns);
            System.out.println("");
            return board;
        }
        // now we are going to randoml put the ships into this
      
        // ship names
        String[] shipNames = new String[5];
        shipNames[0] = "Patrol Boat";
        shipNames[1] = "Cruiser";
        shipNames[2] = "Submarine";
        shipNames[3] = "Battleship";
        shipNames[4] = "Aircraft Carrier";

        // shipLenghts
        int[] shipLenghts = new int[5];
        shipLenghts[0] = 2;
        shipLenghts[1] = 3;
        shipLenghts[2] = 3;
        shipLenghts[3] = 4;
        shipLenghts[4] = 5;
        // now randomly adding the ships
        placeBattleShips(shipLenghts, shipNames, board, rows, columns);
        Printboard.Print(board, rows, columns);
        
        System.out.println();
        return board;

    }
    public static void checkBoard(Cell[][] board, int row ,int column,int boardRows,int boardColumns,BufferedReader reader,PrintWriter write)
    {
       
        // if this is true we have finished checking for other ships 
        //of the same type that were hit
        boolean finishChecking = false;
        // if a ship has been hit this will be set to ship length - 1
        //if 0 then sunk and reduce this by 1 for each ship of the same name that was hit
        String currentShipName = board[row][column].shipName;
        int hitShipLength = 0;
        //keeps track of start and current 
        int startRow = 0;
        int startColumn = 0;
        startRow = row;
        startColumn = column;

        int currentRow = startRow;
        int currentColumn = startColumn;
        int currentDirection = 0; // 0 up 1 right 2 down 3 left
        // if this does not contain ship 

       
        if(!board[row][column].containsShip)
        {
            // send back miss
            char letter;
            letter = AlphabetArray.convertNumberToString(startRow);
            write.println("MISS:" + letter +"-" + (startColumn + 1));
        }else// it does contain a ship
        {
            hitShipLength = board[row][column].shiplength;
            int currentlengthofShip = hitShipLength - 1;
            board[startRow][startColumn].hit = true;
        
            while(true)
            {
               
                if(currentlengthofShip <= 0)
                {
                    break;
                }
               
                if (board[currentRow][currentColumn].containsShip == true && board[currentRow][currentColumn].shipName.equals(currentShipName) && board[currentRow][currentColumn].hit == true) 
                {
                    
                    
    
                    // subtract 1 from the length of ship
                    // for recording the available rows and columns though should only be
                    // max of the boat size to place
                    if (currentDirection == 4) {

                        
                        // reseting everything
                        startRow = row;
                        startColumn = column;

                        currentRow = startRow;
                        currentColumn = startColumn;

                        currentDirection = 0;

                    }
                    // can we move up

                   
                
                    if (board[currentRow][currentColumn].up == true && currentDirection == 0 ) 
                    {
                     
                        if(board[currentRow][currentColumn].shipName.equals(currentShipName))
                        {
                          
                            // decrease our ship lenght
                            if(currentRow != startRow) //only subtract this if we are not on the starting one that was hit as this is already subtracted
                                currentlengthofShip = currentlengthofShip -1;
                     
                            currentRow = currentRow -1;
                            continue;
                        }else
                        {
                            currentDirection = 1; // move to cheking right
                            currentRow = startRow;
                            currentlengthofShip -=1;
                            System.out.println(currentlengthofShip);
                            continue;

                        }
                        

                    } else if (currentDirection == 0) // we cannot continue going up so switch directions
                    {

                        System.out.println("HERE");
                        System.out.println(currentlengthofShip);
                        if(currentRow != startRow)
                            currentlengthofShip -=1;
                        //move to the right 
                      
                        currentDirection = 1;

                        currentRow = startRow;
                        continue;
                    }
                    // right
                    if (board[currentRow][currentColumn].right == true && currentDirection == 1 ) 
                    {
                        if(board[currentRow][currentColumn].shipName.equals(currentShipName))
                        {
             
                            // decrease our ship lenght
                            if(currentColumn != startColumn) //only subtract this if we are not on the starting one that was hit as this is already subtracted
                                currentlengthofShip = currentlengthofShip -1;
                 
                            currentColumn = currentColumn +1;
                         
                            continue;
                        } else
                        {
                            currentDirection = 2;
                            currentRow = startRow;
                            currentColumn = startColumn;
                            continue;
                        }
                       
                    } else if (currentDirection == 1) // we cannot continue going up so switch directions
                    {

                        
                        //move Down
                        currentDirection = 2;
                        currentColumn = startColumn;
                        continue;
                    }

                    // down
                    if (board[currentRow][currentColumn].down == true && currentDirection == 2 ) 
                    {
                       
                        if(board[currentRow][currentColumn].shipName.equals(currentShipName))
                        {
                       
                            // decrease our ship lenght
                            if(currentRow != startRow) //only subtract this if we are not on the starting one that was hit as this is already subtracted
                                currentlengthofShip = currentlengthofShip -1;
          
                            currentRow = currentRow +1;
                            continue;
                        }else
                        {
                            currentDirection = 3; // move to left
                            currentRow = startRow;
                            currentlengthofShip += 1;// we immediately subtract this
                            continue;

                        }
                        

                    } else if (currentDirection == 2) // we cannot continue going up so switch directions
                    {

                        
                        //move to the right 
                        currentDirection = 3;
                        if(currentRow != startRow)
                            currentlengthofShip -=1;
                        currentRow = startRow;
                        continue;
                    }

                     // left
                    if (board[currentRow][currentColumn].left == true && currentDirection == 3 ) 
                    {
                        if(board[currentRow][currentColumn].shipName.equals(currentShipName))
                        {
                       
      
                            // decrease our ship lenght
                            if(currentColumn != startColumn) //only subtract this if we are not on the starting one that was hit as this is already subtracted
                                currentlengthofShip = currentlengthofShip -1;
                          
                        
                            currentColumn = currentColumn -1;
                          
                            continue;
                        } else
                        {
                            currentDirection = 4;
                            currentRow = startRow;
                            currentColumn = startColumn;
                            continue;
                        }
                       
                    } else if (currentDirection == 3) // we cannot continue going up so switch directions
                    {

                        
                        //move to the right 
                        currentDirection = 4;
                      
                        // unless we have already subtracted it
                        if(currentRow != startRow)
                            currentlengthofShip -=1;
                        currentColumn = startColumn;
                        continue;
                    }


                }else
                {
                    //start again and increase current Direction
             
                    if( board[currentRow][currentColumn].shipName.equals(currentShipName) && board[currentRow][currentColumn].hit == false)
                    {
                     
                        
                        break;
                    }
                    
                    currentColumn =startColumn;
                    currentRow =startRow;
                    currentDirection += 1;
              
                    
                  
                   
                }
            }
            if(currentlengthofShip != 0)
            {
                char letter;
                letter = AlphabetArray.convertNumberToString(startRow);
 
                write.println("HIT:" + letter + "-" + (startColumn + 1));
            }
            else
            {
                for( int i = 0; i < sunkenShip.length; i++)
                {
                    if(sunkenShip[i] != null)
                    {
                        if(sunkenShip[i].equals(currentShipName));
                            alreadySunk = true;
                    }
                }
                // if we have already sunk this then do not 
                // subtract from the remaining ships to be sunk
                if(alreadySunk == false)
                    totalShip -= 1;
                else
                    alreadySunk = false;
                // we have lost
                if(totalShip <= 0)
                {

                    gameOver = true;
                    won = false;
                    char letter;
                    letter = AlphabetArray.convertNumberToString(startRow);
                    write.println("GAME END:" + letter + "-" + (startColumn + 1) +":"+ currentShipName);
                }else
                {
                   
                    char letter;
                    letter = AlphabetArray.convertNumberToString(startRow);
                    write.println("SUNK:" + letter +  "-" + (startColumn + 1) + ":"+ currentShipName );
                    // this is done so that when sinking the same ship it does not constantly decrease the remainingships
                    for( int i = 0; i < sunkenShip.length; i++)
                    {
                        if(sunkenShip[i] == null )
                        {
                            sunkenShip[i] = currentShipName;
                        }
                    }
                }
           
            }
               

        }
    }


    public static void createTCPConnection(String receivedMessage) {
        try {

            // these will be used to establish the TCP after UDP established
            ServerSocket tcpServerSocket = null;
            Socket tcpSocket = null;
            int tcpPort = 9001; // TCP port for further communication
            // this means we are player one
            if (!receivedMessage.contains(("NEW GAME"))) {
                playerName = "Player 1";
                currentTurn = true;
                if (tcpSocket == null || tcpSocket.isClosed()) {
                    // estabish what port the server will be on
                    tcpServerSocket = new ServerSocket(tcpPort);
                    System.out.println("Accepting");
                    tcpSocket = tcpServerSocket.accept(); // acept

                    // now the buffer reader and writer
                    BufferedReader reader = new BufferedReader(new InputStreamReader(tcpSocket.getInputStream()));
                    PrintWriter writer = new PrintWriter(tcpSocket.getOutputStream(), true);

                    // now just testing this out to see if it has worked
                    writer.println("Hello from Player Two");
                    writer.flush();
                    // getting the response
                    String response = reader.readLine();
                    System.out.println("Recevied From player One" + response);
                    
                    
                  
                    // now greating a board 10 by 10 the smallest
              
                    Cell[][] board;
                    Cell[][] otherPlayerBoard;
                    // 0 means this player 1 means opponents
            
                    board = createGrid(gridRowSize, gridColumnSize,0);
            
                    otherPlayerBoard = createGrid(gridRowSize, gridColumnSize, 1);
               
                    //waiting for a response from player 2 to determine when they are ready 
                    System.out.println("waiting for a response from player two confirming grid creation");
                    
                 
                 
                    //now firing 
                    while(gameOver == false)
                    {
                        
                        // if it is our turn the fire wait for reslts 
                        // and then set our turn to false
                  
                        if(currentTurn == true)
                        {
                         
                            fireOperation(reader,writer,  gridRowSize, gridColumnSize);
                    
                            response = reader.readLine();
                            
                            currentTurn = false;
                            // update the enemy board at fireRow and columnRow
                            if(response.contains("MISS"))
                            {
                                  // the -1 is because we do not account starting at 0
                                otherPlayerBoard[firedRow-1][firedColumn-1].miss = true;
                                Printboard.Print(board, gridRowSize, gridColumnSize);
                                System.out.println();
                                Printboard.Print(otherPlayerBoard,gridRowSize, gridColumnSize);
                                System.out.println();
                            }else if(response.contains("HIT"))
                            {
                                 // the -1 is because we do not account starting at 0
                                otherPlayerBoard[firedRow-1][firedColumn-1].hit = true;
                                Printboard.Print(board, gridRowSize, gridColumnSize);
                                System.out.println();
                                Printboard.Print(otherPlayerBoard,gridRowSize, gridColumnSize);
                                System.out.println();
                            }else if(response.contains("SUNK"))
                            {
                                // the -1 is because we do not account starting at 0
                                Printboard.Print(board, gridRowSize, gridColumnSize);
                                System.out.println();
                                otherPlayerBoard[firedRow-1][firedColumn-1].hit = true;
                                Printboard.Print(otherPlayerBoard,gridRowSize, gridColumnSize);
                                System.out.println();
                            }
                            System.out.println(response);
                        }   
                        else// we are waiting for the coordinates from the other player
                        {
                            //now this is where things will get more computational
                            //
                            int hitRow = 0; 
                            int hitColumn = 0;
                            System.out.println("Waiting for other players turn");
                            response = reader.readLine();
                            System.out.println(response);
                            hitRow = Integer.parseInt(response) - 1;
                            response = reader.readLine();
                            hitColumn= Integer.parseInt(response) - 1;
                            
                            // checing if this has hit something or not
                            checkBoard(board,hitRow,hitColumn, gridRowSize,gridColumnSize,reader,writer);
                            currentTurn = true;
             
                        }
                    }
                    System.out.println("GAME OVER" + gameOver);
                    if(won == true)
                    {

                        
                        System.out.println("YOU HAVE WON");
                    }else
                    {
                       
                       System.out.println("YOU HAVE LOST");
                    }
                    

                }

                // this be player two
            } else if (receivedMessage.contains("NEW GAME")) // the other player sent the message and we want to listen
                                                             // now
            {
                
             
                playerName = "Player 2";
                currentTurn = false;
             
                // need to make sure there is on created on a port before we do this
              
                // we are loocking at this port on the local for the TCP connection
                tcpSocket = new Socket("127.0.0.1", tcpPort);

                // now the buffer reader and writer
                BufferedReader reader = new BufferedReader(new InputStreamReader(tcpSocket.getInputStream()));
                PrintWriter writer = new PrintWriter(tcpSocket.getOutputStream(), true);

                // now waiting for an input
                String response = reader.readLine();
                System.out.println(response);

                // sending out a default message

                writer.println("Hello");
                writer.flush();


                // now greating a board 10 by 10 the smallest
              
                Cell[][] board;
                Cell[][] otherPlayerBoard;
                // 0 means this player 1 means opponents
             
                board = createGrid(gridRowSize, gridColumnSize,0);
                otherPlayerBoard = createGrid(gridRowSize, gridColumnSize, 1);
                //now firing 
                while(gameOver == false)
                    {
                        // if it is our turn the fire wait for reslts 
                        // and then set our turn to false
                       
                        if(currentTurn == true)
                        {
                         
                            fireOperation(reader,writer, gridRowSize ,gridColumnSize);
                         
                            response = reader.readLine();
                            System.out.println(response);
                            currentTurn = false;
                            // update the enemy board at fireRow and columnRow
                            if(response.contains("MISS"))
                            {
                                // the -1 is because we do not account starting at 0
                                otherPlayerBoard[firedRow-1][firedColumn-1].miss = true;
                                Printboard.Print(board, gridRowSize, gridColumnSize);
                                System.out.println();
                                Printboard.Print(otherPlayerBoard,gridRowSize, gridColumnSize);
                                System.out.println();
                            }else if(response.contains("HIT"))
                            {
                                // the -1 is because we do not account starting at 0
                                Printboard.Print(board, gridRowSize, gridColumnSize);
                                System.out.println();
                                otherPlayerBoard[firedRow-1][firedColumn-1].hit = true;
                                Printboard.Print(otherPlayerBoard,gridRowSize, gridColumnSize);
                                System.out.println();
                            }else if(response.contains("SUNK"))
                            {
                                // the -1 is because we do not account starting at 0
                                Printboard.Print(board, gridRowSize, gridColumnSize);
                                System.out.println();
                                otherPlayerBoard[firedRow-1][firedColumn-1].hit = true;
                                Printboard.Print(otherPlayerBoard,gridRowSize, gridColumnSize);
                                System.out.println();
                            }
                            System.out.println(response);
                        }   
                        else// we are waiting for the coordinates from the other player
                        {
                            //now this is where things will get more computational
                            //
                            int hitRow = 0; 
                            int hitColumn = 0;
                            System.out.println("Waiting for other players turn");
                            response = reader.readLine();

                            hitRow = Integer.parseInt(response) - 1;
                            response = reader.readLine();
                            hitColumn= Integer.parseInt(response) - 1;
                     
                            // checing if this has hit something or not
                            checkBoard(board,hitRow,hitColumn, gridRowSize,gridColumnSize,reader,writer);
                           
                            currentTurn = true;
             
                        }
                    }
                    System.out.println("GAME OVER" + gameOver);
                    if(won == true)
                    {
                        tcpSocket.close();
                        System.out.println("YOU HAVE WON");
                    }else
                    {
                        tcpSocket.close();
                       System.out.println("YOU HAVE LOST");
                    }
                    
                // establishTCP(tcpServerSocket,tcpSocket,tcpPort);
        
    
            }
        } catch (Exception e) {
            // TODO: handle exception
        }
      
    }



    public static void main(String[] args) {

        DatagramSocket socket = null;
        int port = 9001;
        boolean isFirstIteration = true;

        try {
            socket = new DatagramSocket(port);
            //socket.setSoTimeout(300); // Set a 30-second timeout for receiving data

            while (true) {
                try {
                 

                    byte[] receiveData = new byte[1024];
                    DatagramPacket receivePacket = new DatagramPacket(receiveData, receiveData.length);

                    // Listen for incoming data
                    System.out.println("Waiting");
                    socket.receive(receivePacket);
                    String receivedMessage = new String(receivePacket.getData(), 0, receivePacket.getLength());
                    InetAddress senderAddress = receivePacket.getAddress();
                    int senderPort = receivePacket.getPort();
    
                    if(receivedMessage.contains("NEW GAME"))
                    {

                  
                        String responseMessage = "Establish TCP";
                        byte[] responseData = responseMessage.getBytes();
                        DatagramPacket responsePacket = new DatagramPacket(responseData, responseData.length, senderAddress, senderPort);
                        socket.send(responsePacket);
                        // getting the required data from the message row column and port
                        String[] parts = receivedMessage.split(":"); // Split the string using ":"
                        tcpPort = Integer.parseInt(parts[1]);
                        gridRowSize = Integer.parseInt(parts[2]);
                        gridColumnSize = gridRowSize;

                    }
                    System.out.println(receivedMessage);
             
                   
                    //String receivedMessage = new String(receivePacket.getData(), 0, receivePacket.getLength());
                    // create the TCP connection
                    createTCPConnection(receivedMessage);
               
                    System.out.println("EVERYTHING WORKED");
                    socket.close();
                    break;

                    
                    
                    // we are sending not lisetning any more
                } catch (SocketTimeoutException e) {
                    // No data received within 30 seconds, send a broadcast on the current port
                    gridSize = 10;
                    gridRowSize = gridSize;
                    gridColumnSize = gridSize;
                    InetAddress broadcastAddress = InetAddress.getByName("127.0.0.1");
                    String message = "NEW GAME:9001:" + gridSize;
                    byte[] sendData = message.getBytes();

                    DatagramPacket sendPacket = new DatagramPacket(sendData, sendData.length, broadcastAddress, port);
                    socket.send(sendPacket);

                    System.out.println("Sent broadcast on port " + port);

                    if (port == 9100 && isFirstIteration == false) {
                        port = 9000; // Reset to 9000 after reaching 9100
                    } else if (isFirstIteration == true) {
                        isFirstIteration = false;
                        port = 9000;
                    } else {
                        port++; // Increment the port number
                    }

                    System.out.println("Listening on port " + port); // Print the new port being listened to
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (socket != null && !socket.isClosed()) {
                socket.close();
            }
        }
    }
}
