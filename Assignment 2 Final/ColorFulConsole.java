public class ColorFulConsole {
    public static void main(String[] args) {
        // ANSI escape codes for text color
        String redColor = "\u001B[31m";
        String greenColor = "\u001B[32m";
        String resetColor = "\u001B[0m"; // Reset to default color

        // Printing text in red
        System.out.println(redColor + "This is red text." + resetColor);

        // Printing text in green
        System.out.println(greenColor + "This is green text." + resetColor);
    }
}
