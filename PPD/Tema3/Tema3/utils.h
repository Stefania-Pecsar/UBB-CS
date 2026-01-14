#pragma once
#ifndef UTILS_H
#define UTILS_H
#include <stdio.h>

#include <vector>
#include <string>

// Function declarations (prototypes)
std::vector<int> generateRandomVector(int size);
void saveVectorToFile(const std::vector<int>& vector, const char* fileName);
std::vector<int> readVectorFromFile(const char* fileName);
std::vector<int> readVectorFromFileManipulated(const char* fileName, int start, int end);
std::vector<int> reverseVector(const std::vector<int>& vector);
std::vector<int> readLargeNumber(const std::string& filename);
void createvectors();
void printVector(const std::vector<int>& vec);
std::vector<int> removeLeadingZeros(const std::vector<int>& vec);

std::vector<int> reverseVector(const std::vector<int>& vec);
std::pair<std::vector<int>, int> addLargeNumbers(const std::vector<int>& vec1, const std::vector<int>& vec2, int initialCarry);

#endif