#include <cmath>
#include <cstdlib>
#include <ctime>
#include <iostream>
#include <limits>
#include <vector>

#define numCustomers 5  // including depot which is at index 0
#define maxVehicles 4
#define ALPHA 1
#define BETA 1
#define EVAPORATION_RATE 0.1
#define ITERATIONS 2000
#define CAPACITY 15

using namespace std;

// Random function to generate a number between 0 and 1
double randomDouble() {
    return (double)rand() / (RAND_MAX);
}

double timeMatrix[numCustomers][numCustomers] = {
    {0, 8, 6, 7, 3},
    {8, 0, 5, 9, 4},
    {6, 5, 0, 4, 2},
    {7, 9, 4, 0, 5},
    {3, 4, 2, 5, 0}

};

double pheromoneMatrix[numCustomers][numCustomers];

// demand for depot is 0
int demand[numCustomers] = {0, 10, 15, 7, 12};

// Function to calculate the probability distribution for an ant's next move
int selectNextCity(int currentCity, vector<bool>& visited, int currentDemand) {
    vector<double> probabilities(numCustomers, 0);
    double sum = 0.0;

    for (int i = 0; i < numCustomers; i++) {
        if (!visited[i] && i != currentCity && demand[i] + currentDemand <= CAPACITY) {
            probabilities[i] = pow(pheromoneMatrix[currentCity][i], ALPHA) * pow(1.0 / timeMatrix[currentCity][i], BETA);
            sum += probabilities[i];
        }
    }

    for (int i = 0; i < numCustomers; i++) {
        probabilities[i] /= sum;
    }

    // Select the next city based on the probability distribution
    // it will select customer who are not isited and respects the deman limits also
    double r = randomDouble();
    double cumulative = 0.0;
    for (int i = 0; i < numCustomers; i++) {
        cumulative += probabilities[i];
        if (r <= cumulative) {
            return i;
        }
    }
    return -1;
}

double calculateTourTime(vector<int>& tour) {
    double length = 0.0;
    for (int i = 0; i < tour.size() - 1; i++) {
        length += timeMatrix[tour[i]][tour[i + 1]];
    }
    length += timeMatrix[tour.back()][0];  // Return to depot
    return length;
}

// double calculateTourTimeD(vector<int>& tour) {
//     double length = 0.0;
//     for (int i = 0; i < tour.size() - 1; i++) {
//         cout<<tour[i]<<" "<<tour[i+1]<<" "<<timeMatrix[tour[i]][tour[i+1]]<<endl;

//         length += timeMatrix[tour[i]][tour[i + 1]];
//     }

//     return length;
// }

// Function to update the pheromone matrix based on the ants' tours
void updatePheromones(vector<vector<int>>& allTours, vector<double>& tourLengths) {
    // Evaporate pheromones
    for (int i = 0; i < numCustomers; i++) {
        for (int j = 0; j < numCustomers; j++) {
            pheromoneMatrix[i][j] *= (1 - EVAPORATION_RATE);
        }
    }

    // Deposit pheromones based on the ants' tours
    for (int ant = 0; ant < maxVehicles; ant++) {
        if (tourLengths[ant] == 0) continue;  // Skip unused vehicles

        for (int i = 0; i < allTours[ant].size() - 1; i++) {
            int u = allTours[ant][i];
            int v = allTours[ant][i + 1];
            pheromoneMatrix[u][v] += 1.0 / tourLengths[ant];
            pheromoneMatrix[v][u] += 1.0 / tourLengths[ant];
        }
        int u = allTours[ant].back();
        pheromoneMatrix[u][0] += 1.0 / tourLengths[ant];  // Return to depot
        pheromoneMatrix[0][u] += 1.0 / tourLengths[ant];
    }
}

int main() {
    srand(time(0));  // Seed for randomness

    // Initialize pheromone matrix with a small positive value
    for (int i = 0; i < numCustomers; i++) {
        for (int j = 0; j < numCustomers; j++) {
            pheromoneMatrix[i][j] = 1.0;
        }
    }

    vector<vector<int>> bestTours(maxVehicles);
    vector<double> bestTourLengths(maxVehicles, numeric_limits<double>::max());
    int bestVehicleCount = maxVehicles;  // Start with the max number of vehicles used

    // Main loop
    for (int iter = 0; iter < ITERATIONS; iter++) {
        vector<vector<int>> allTours(maxVehicles);  // Each vehicle has its own tour
        vector<double> tourLengths(maxVehicles, 0.0);
        vector<int> vehicleCounts(maxVehicles, 0);  // Track number of vehicles used

        // Initialize visited cities
        vector<bool> visited(numCustomers, false);
        visited[0] = true;  // Depot is always visited at the start

        // Each vehicle constructs a tour
        for (int ant = 0; ant < maxVehicles; ant++) {
            int currentCity = 0;  // Start from the depot
            int currentDemand = 0;

            allTours[ant].push_back(currentCity);  // Start at depot

            while (true) {
                int nextCity = selectNextCity(currentCity, visited, currentDemand);
                if (nextCity == -1) {
                    break;  // No valid city to visit, go back to depot
                }

                allTours[ant].push_back(nextCity);
                visited[nextCity] = true;
                currentDemand += demand[nextCity];
                currentCity = nextCity;

                // Check if all customers are visited
                bool allVisited = true;
                for (int i = 1; i < numCustomers; i++) {
                    if (!visited[i]) {
                        allVisited = false;
                        break;
                    }
                }
                if (allVisited) break;
            }

            // Complete the tour by returning to the depot
            allTours[ant].push_back(0);

            // Calculate tour length
            tourLengths[ant] = calculateTourTime(allTours[ant]);
        }

        // Count how many vehicles were actually used
        int vehicleCount = 0;
        for (int ant = 0; ant < maxVehicles; ant++) {
            if (allTours[ant].size() > 2) {  // A vehicle used if it has more than depot visit
                vehicleCount++;
            }
        }

        // If fewer vehicles used or same number with shorter tour length, update best tour
        double totalTourLength = 0.0;
        for (int ant = 0; ant < maxVehicles; ant++) {
            totalTourLength += tourLengths[ant];
        }

        if (vehicleCount < bestVehicleCount || (vehicleCount == bestVehicleCount && totalTourLength < bestTourLengths[0])) {
            bestVehicleCount = vehicleCount;
            bestTours = allTours;
            bestTourLengths = tourLengths;
        }

        // Update pheromones
        updatePheromones(allTours, tourLengths);

        cout << "Iteration " << iter + 1 << ": Best total tour length = " << totalTourLength << ", Vehicles used = " << vehicleCount << endl;
    }

    // Print the best tours for each vehicle and their corresponding time costs
    for (int ant = 0; ant < maxVehicles; ant++) {
        if (bestTours[ant].size() > 2) {  // Only print vehicles that have non-trivial tours
            cout << "Vehicle " << ant + 1 << " path: ";
            for (int i = 0; i < bestTours[ant].size(); i++) {
                cout << bestTours[ant][i] << " ";
            }

            cout << "\nTotal travel time: " << bestTourLengths[ant] << endl;
        }
    }

    return 0;
}