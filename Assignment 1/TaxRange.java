// this will and individual range for the tax ranges 
// will be stored in an array
public class TaxRange 
{
    private int start;
    private int end;
    private int baseTax;
    private int taxPerDollar;

    public TaxRange(int start,int end, int baseTax, int taxPerDollar)
    {
        this.start = start;
        this.end = end;
        this.baseTax = baseTax;
        this.taxPerDollar = taxPerDollar;
    }

    public void setStart(int value)
    {
        this.start = value;
    }
    public void setEnd(int value)
    {
        this.end = value;
    }
    public void setBaseTax(int value)
    {
        this.baseTax = value;
    }
    public void setTaxPerDollar(int value)
    {
        this.taxPerDollar = value;
    }
    public int getStart()
    {
        return this.start;
    }
    public int getEnd()
    {
        return this.end;
    }
    public int getBaseTax()
    {
        return this.baseTax;
    }
    public int getTaxPerDollar()
    {
        return this.taxPerDollar;
    }
    
}
