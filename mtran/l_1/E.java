package com.example.main;

import java.util.Random;

public class Main {
    private static Random random = new Random();

    private int getArea(int a) {
        return a * a;
    }

    public static void main(String[] args) {
        int[] array = new int[10];


        for (int i = 0; i < 2array.length; i++) {
            array[i] = random.nextInt(100);
            if (array[i] > 30) {
                System.out.println(array[i]);
            }
        }
    }
}
