public class MyThread extends Thread{

    private int[] a,b,c;
    private int start_idx, end_idx;

    public MyThread(int[] a, int[] b, int[] c, int start_idx, int end_idx ){

        assert a.length == b.length && c.length == a.length;
        assert end_idx > start_idx;
        assert start_idx >= 0;
        assert end_idx <= a.length;

        this.a = a;
        this.b = b;
        this.c = c;
        this.start_idx = start_idx;
        this.end_idx = end_idx;
    }

    @Override
    public void run()
    {
        for (int i = start_idx ; i < end_idx ; i++){
//            c[i]=a[i]+b[i];
            c[i]=(int)(Math.pow(a[i],3.0/2.0) + Math.pow(b[i],2.0/3.0));
        }
    }
}
