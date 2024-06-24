# Shamir for ed25519 with PHE

This is an implementation of Shamir's Secret Sharing Scheme for Symbol PrivateKeys, enhanced with Partial Homomorphic Encryption (PHE) for added security.


## Usage

Setup the environment and run the script:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Start the script:

```bash
sh entrypoint.sh
```

## Example

This API server can split an ed25519 private key using Shamir's Secret Sharing. The ed25519 private key is 32 bytes of binary data. According to the specifications, after splitting the key into two parts, five shares are generated for each part.

By collecting three or more of the created five shares, the original private key can be restored.

```bash
ed25519 private key: D72E99DE4A5F44BD2E59C33FD023FAB3797441B72EEF28B19B28EFF45E902311

↓

key 1: D72E99DE4A5F44BD2E59C33FD023FAB3
key 2: 797441B72EEF28B19B28EFF45E902311

↓

share 1: 
  tuple(0, xxxxxxxxxxxxxxxxxxxxxxxxxxx)
  tuple(1, xxxxxxxxxxxxxxxxxxxxxxxxxxx)
  tuple(2, xxxxxxxxxxxxxxxxxxxxxxxxxxx)
  tuple(3, xxxxxxxxxxxxxxxxxxxxxxxxxxx)
  tuple(4, xxxxxxxxxxxxxxxxxxxxxxxxxxx)
share 2: 
  tuple(0, xxxxxxxxxxxxxxxxxxxxxxxxxxx)
  tuple(1, xxxxxxxxxxxxxxxxxxxxxxxxxxx)
  tuple(2, xxxxxxxxxxxxxxxxxxxxxxxxxxx)
  tuple(3, xxxxxxxxxxxxxxxxxxxxxxxxxxx)
  tuple(4, xxxxxxxxxxxxxxxxxxxxxxxxxxx)
```

## Partial Homomorphic Encryption (PHE)

In addition to Shamir's Secret Sharing, this implementation also utilizes Partial Homomorphic Encryption (PHE) to provide an extra layer of security. PHE allows computations to be performed on encrypted data without revealing the underlying values.

Here's how PHE is integrated into the secret sharing process:

1. **Key Generation**:
   - Generate a public-private key pair for the PHE scheme (e.g., Paillier cryptosystem).

2. **Share Encryption**:
   - After generating the shares using Shamir's Secret Sharing, encrypt each share using the PHE public key.
   - The encrypted shares are then distributed to the participants.

3. **Secure Computation**:
   - Participants can perform computations on the encrypted shares without revealing the actual values.
   - This allows for secure multi-party computation and collaboration.

4. **Share Decryption and Reconstruction**:
   - When enough encrypted shares are collected, they are decrypted using the PHE private key.
   - The decrypted shares are then used to reconstruct the original secret using Shamir's Secret Sharing reconstruction process.

By combining Shamir's Secret Sharing with PHE, the security and privacy of the shared secret are enhanced. Even if an attacker gains access to the encrypted shares, they cannot recover the original secret without the PHE private key.

## Note

Sure, here is the explanation in English using a quadratic polynomial example $y = ax^2 + bx + c$:

### Basic Concept

Shamir's Secret Sharing method divides a secret (e.g., a password or a cryptographic key) into multiple "shares" such that the secret can only be reconstructed when a sufficient number of shares are combined.

### Step-by-Step Explanation

1. **Determine the Secret**:
   - Let's take a secret number, for example, 42.

2. **Create the Polynomial**:
   - Form a polynomial where the secret is the constant term. Use random coefficients for the other terms. For example, let's use:
     $y = ax^2 + bx + c$
   - Suppose $a = 3$, $b = 5$, and the secret $c = 42$. The polynomial becomes:
     $y = 3x^2 + 5x + 42$

3. **Generate Shares**:
   - Evaluate the polynomial at different values of $x$. For instance:
     - When $x = 1$: $y = 3(1)^2 + 5(1) + 42 = 50$ → Share is (1, 50)
     - When $x = 2$: $y = 3(2)^2 + 5(2) + 42 = 68$ → Share is (2, 68)
     - When $x = 3$: $y = 3(3)^2 + 5(3) + 42 = 96$ → Share is (3, 96)
     - When $x = 4$: $y = 3(4)^2 + 5(4) + 42 = 134$ → Share is (4, 134)
     - When $x = 5$: $y = 3(5)^2 + 5(5) + 42 = 182$ → Share is (5, 182)

4. **Distribute Shares**:
   - Distribute these shares to different participants. For example, give the shares (1, 50), (2, 68), (3, 96), (4, 134), and (5, 182) to five people.

5. **Reconstruct the Secret**:
   - To reconstruct the secret, at least three shares are needed. Suppose we have shares (1, 50), (2, 68), and (3, 96).
   - Use these shares to reconstruct the original polynomial using the Lagrange interpolation formula:
     $L(x) = \sum_{i=1}^{3} y_i \prod_{j=1, j \ne i}^{3} \frac{x - x_j}{x_i - x_j}$
     - $L_1(x)$ corresponds to the term for $x = 1$
     - $L_2(x)$ corresponds to the term for $x = 2$
     - $L_3(x)$ corresponds to the term for $x = 3$

6. **Calculate Coefficients**:
   - Plug the share values into the Lagrange interpolation formula to determine the coefficients.
   - The result is the original polynomial $y = 3x^2 + 5x + 42$, and the secret $c = 42$ is recovered when $x = 0$.

### Why It Is Secure

- With fewer than 3 shares, it is impossible to reconstruct the polynomial and therefore the secret remains safe.
- With 3 or more shares, the polynomial can be reconstructed accurately, revealing the secret.

This ensures that the secret can only be known when a sufficient number of shares are combined, providing a robust security mechanism.

## Secure Multi-Party Computation (MPC)*Implemented in the future test

Secure Multi-Party Computation (MPC) is a cryptographic technique that allows multiple parties to jointly compute a function over their inputs while keeping those inputs private. In the context of this implementation, MPC can be used to perform computations on the encrypted shares without revealing the underlying values.

Here's how MPC can be integrated into the secret sharing and PHE process:

1. **Distributed Computation**:
   - Participants engage in an MPC protocol to perform computations on their encrypted shares.
   - The MPC protocol ensures that each participant can contribute to the computation without revealing their individual shares.

2. **Secure Aggregation**:
   - The MPC protocol securely aggregates the results of the distributed computation.
   - The aggregated result is still encrypted and does not reveal any information about the individual shares.

3. **Threshold Decryption**:
   - Once the aggregated result is obtained, a threshold decryption scheme can be used to decrypt the result.
   - Threshold decryption requires a minimum number of participants to collaborate and combine their partial decryption keys to recover the final result.

By incorporating MPC into the secret sharing and PHE process, additional security and privacy guarantees can be achieved. Participants can perform computations on the encrypted shares without revealing their individual values, and the final result can only be obtained through collaborative decryption.

## Conclusion

This implementation combines Shamir's Secret Sharing, Partial Homomorphic Encryption (PHE), and Secure Multi-Party Computation (MPC) to provide a robust and secure solution for splitting and reconstructing private keys. By leveraging these cryptographic techniques, the privacy and confidentiality of the shared secret are maintained throughout the process, even in the presence of malicious participants or adversaries.

Please note that the code provided in this repository is for demonstration purposes and may require further security enhancements and optimizations for production use. It is recommended to thoroughly review and audit the code before deploying it in a real-world scenario.

For more information on the underlying cryptographic concepts and their security properties, please refer to the relevant academic literature and research papers.