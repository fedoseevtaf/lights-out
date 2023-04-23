import numpy as np


def build_matrix(n):
	rows = [None] * (n * n)
	for i in range(n):
		for j in range(n):
			rows[i * n + j] = [0] * (n * n)
			if i > 0:
				rows[i * n + j][(i - 1) * n + j] = 1
			if i + 1 < n:
				rows[i * n + j][(i + 1) * n + j] = 1
			if j > 0:
				rows[i * n + j][i * n + j - 1] = 1
			if j + 1 < n:
				rows[i * n + j][i * n + j + 1] = 1
			rows[i * n + j][i * n + j] = 1
	return np.array(rows)

def gauss(A, b):
	A, b = A.copy(), b.copy()
	n = len(b)
	indices = [None] * n
	row = 0
	for col in range(n):
		for i in range(row, n):
			if A[i][col]:
				A[i], A[row] = A[row], A[i]
				b[i], b[row] = b[row], b[i]
				break
		else:
			continue
		indices[col] = row
		for i in range(n):
			if i != row and A[i][col]:
				A[i] ^= A[row]
				b[i] ^= b[row]
		row += 1

	ans = np.zeros(n, dtype=int)
	for i in range(n):
		if indices[i] is not None:
			ans[i] = b[indices[i]]
	if any((A @ ans) % 2 != b):
		return None
	return ans


if __name__ == '__main__':
    A = build_matrix(3)
    # b = np.zeros(3 * 3)
    b = np.array([0, 0, 0, 1, 1, 0, 0, 0, 1])
    x = gauss(A, b)
    print(A, x, b, (A @ x) % 2, sep='\n\n')
