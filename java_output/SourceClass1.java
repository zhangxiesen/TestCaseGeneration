package test.extractmethod;

public class SourceClass1 {
    
    public void refMethod() {
        int number = 50; /*EXTRACT*/
        if (number > 0) {
            System.out.println("Number is positive.");
        } else {
            System.out.println("Number is not positive.");
        }
    }

    public static void main(String[] args) {
        SourceClass1 obj = new SourceClass1();
        obj.refMethod();
    }
}