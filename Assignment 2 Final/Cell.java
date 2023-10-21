
//what each cell contains
public class Cell 
{
    public boolean hit = false;
    public boolean miss = false;
    public boolean containsShip = false;
    // this will be a number from 1 to however many ships there are
    public int shiplength = 0;
    public String shipName = "";
    // maybe used for determining if all ships have been hit
    public int remainingShipsSpaces = shiplength;
    //these are just for determining if we can check left right up or donw on the board
    public boolean left = true;
    public boolean right = true;
    public boolean up = true;
    public boolean down = true;


}

