public class AlphabetArray{
    public static int  convertLetterToNumber(String target) 
    {
        // Create an array to store capital letters in the alphabet
        char[] alphabet = new char[26];
        int correspondingNumber = 0;
        // Fill the array with capital letters from 'A' to 'Z'
        for (char letter = 'A'; letter <= 'Z'; letter++) {
            alphabet[letter - 'A'] = letter;
        }

        int[] alphabetValue = new int[26];
        // Print the capital letters and associated numbers
        for (int i = 0; i < alphabet.length; i++) {
            char letter = alphabet[i];
            int number = i + 1;
            alphabetValue[i] = number;
            
        }

        
        // find the corresponding number for the target and return 
        for (int i = 0; i < 26; i++ )
        {
            
           
            if(target.equals(String.valueOf(alphabet[i])))
            {
               
                correspondingNumber = alphabetValue[i];
               
            }
        }
      
        return correspondingNumber;
    }
    // return the charactger instead
    public static char  convertNumberToString(int target) 
    {
        // Create an array to store capital letters in the alphabet
        char[] alphabet = new char[26];

        // Fill the array with capital letters from 'A' to 'Z'
        for (char letter = 'A'; letter <= 'Z'; letter++) {
            alphabet[letter - 'A'] = letter;
        }

        
        return alphabet[target];
    }
}
