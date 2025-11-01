public class Main{
    public static void main(String[] args){
        MyThread t = new MyThread();
        t.start();
        System.out.println("Hello world!");
        t.join();
        System.out.println("Joined thread!");

    }
}