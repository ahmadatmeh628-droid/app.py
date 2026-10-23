// Mobility (Degrees of Freedom) Calculator
// Flow: Planar or Spatial
//   Planar  -> method fi  OR  method nj (nj' and nj'')
//   Spatial -> Revolute, Cylinder, Sphere
#include <iostream>
#include <limits>
#include <string>
using namespace std;

// Read an integer >= minVal (keeps asking until the input is valid)
int readInt(const string& prompt, int minVal) {
    int v;
    while (true) {
        cout << prompt;
        if (cin >> v && v >= minVal) return v;
        cout << "  Invalid input, try again.\n";
        cin.clear();
        cin.ignore(numeric_limits<streamsize>::max(), '\n');
    }
}

// Read a choice that must be 1 or 2
int readChoice(const string& prompt) {
    while (true) {
        int c = readInt(prompt, 1);
        if (c == 1 || c == 2) return c;
        cout << "  Please enter 1 or 2.\n";
    }
}

// Planar: > 0 mechanism, <= 0 not mechanism
void planarResult(int df) {
    cout << "DF = " << df << "\n";
    cout << "Result: " << (df > 0 ? "MECHANISM" : "NOT MECHANISM") << "\n";
}

// Spatial: > 0 mechanism, = 0 static spatial, < 0 not mechanism
void spatialResult(int df) {
    cout << "DF = " << df << "\n";
    if (df > 0)       cout << "Result: MECHANISM\n";
    else if (df == 0) cout << "Result: STATIC SPATIAL\n";
    else              cout << "Result: NOT MECHANISM\n";
}

// ---------- Planar, method fi ----------
// Lower pair (surface contact): fi = 1, nc = 3 - 1 = 2
// Higher pair (point/line contact): fi = 2, nc = 3 - 2 = 1
// DF = 3(nL - nj - 1) + sum(fi)      (nj = lower + higher)
void planarFi() {
    int nL    = readInt("Number of links (with frame): ", 1);
    int nLow  = readInt("Number of Lower joints: ", 0);
    int nHigh = readInt("Number of Higher joints: ", 0);

    int nj     = nLow + nHigh;
    int sumFi  = 1 * nLow + 2 * nHigh;
    int nc     = 2 * nLow + 1 * nHigh;
    int df     = 3 * (nL - nj - 1) + sumFi;

    cout << "\n------ Result ------\n";
    cout << "Lower : fi = 1, nc = 2\n";
    cout << "Higher: fi = 2, nc = 1\n";
    cout << "Total fi = " << sumFi << "\n";
    cout << "Total nc = " << nc << "\n";
    planarResult(df);
}

// ---------- Planar, method nj ----------
// DF = 3(nL-1) - 2*nj' - nj''
void planarNj() {
    int nL  = readInt("Number of links (with frame): ", 1);
    int nj1 = readInt("Number of 1-DF joints (nj'): ", 0);
    int nj2 = readInt("Number of 2-DF joints (nj''): ", 0);

    int nc1 = 3 - 1;   // 1-DF joint
    int nc2 = 3 - 2;   // 2-DF joint
    int sumFi = 1 * nj1 + 2 * nj2;
    int nc    = nc1 * nj1 + nc2 * nj2;
    int df    = 3 * (nL - 1) - nc;

    cout << "\n------ Result ------\n";
    cout << "nj' : fi = 1, nc = " << nc1 << "\n";
    cout << "nj'': fi = 2, nc = " << nc2 << "\n";
    cout << "Total fi = " << sumFi << "\n";
    cout << "Total nc = " << nc << "\n";
    planarResult(df);
}

// ---------- Spatial ----------
// nc = 6 - fi,  DF = 6(nL-1) - nc_total
// Revolute: fi=1 (nc=5) | Cylinder: fi=2 (nc=4) | Sphere: fi=3 (nc=3)
void spatial() {
    int nL = readInt("Number of links (with frame): ", 1);
    int nR = readInt("Number of Revolute joints: ", 0);
    int nC = readInt("Number of Cylinder joints: ", 0);
    int nS = readInt("Number of Sphere joints: ", 0);

    int ncR = 6 - 1;
    int ncC = 6 - 2;
    int ncS = 6 - 3;
    int nc  = ncR * nR + ncC * nC + ncS * nS;
    int df  = 6 * (nL - 1) - nc;

    cout << "\n------ Result ------\n";
    cout << "Revolute: fi = 1, nc = " << ncR << "\n";
    cout << "Cylinder: fi = 2, nc = " << ncC << "\n";
    cout << "Sphere  : fi = 3, nc = " << ncS << "\n";
    cout << "Total nc = " << nc << "\n";
    spatialResult(df);
}

int main() {
    char again;
    do {
        cout << "\n===== Mobility Calculator =====\n";
        cout << "1) Planar\n2) Spatial\n";
        int type = readChoice("Choose: ");

        if (type == 2) {
            spatial();
        } else {
            cout << "Method:\n1) fi\n2) nj\n";
            int method = readChoice("Choose: ");
            if (method == 1) planarFi();
            else             planarNj();
        }

        cout << "\nRun again? (y/n): ";
        cin >> again;
    } while (again == 'y' || again == 'Y');

    return 0;
}
    
