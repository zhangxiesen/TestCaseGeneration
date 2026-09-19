package test.extractvar;

public class SourceClass1 {

    private int value;

    public SourceClass1(int value) {
        this.value = value;
    }

    public void refMethod(int parameter) {
        // Early return conditions
        if (parameter == 0) return;
        if (this.value == 0) return;
        if (parameter + this.value == 0) return;
        if ((parameter - this.value) == 0) return;

        // Extracted variable as an array
        int[] numbers = /*EXTRACT*/ { parameter, this.value };

        // Object array initialized with the current instance
        Object[] objects = { this };

        // Recursive calls
        refMethod(parameter - 1);
        refMethod(parameter - 1);

        // Print statements to ensure method progresses (can be removed in actual test)
        System.out.println("Numbers: " + numbers[0] + ", " + numbers[1]);
        System.out.println("Object: " + objects[0]);
    }

    public static void main(String[] args) {
        SourceClass1 sc = new SourceClass1(5);
        sc.refMethod(3);
    }
}