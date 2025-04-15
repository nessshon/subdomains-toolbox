# TON DNS Subdomains Toolbox

A set of tools for working with subdomains in the TON Blockchain, including smart contracts, a metadata generation API, and a step-by-step usage guide.

## Repository Structure

### `GUIDE.md`

A [step-by-step guide](GUIDE.md) for deploying and using the components of this repository. It includes:

- Deploying smart contracts
- Managing subdomains and records
- Setting up the metadata generation API

---

### `manager-contract/`

A [smart contract](manager-contract) for managing subdomains without NFTs.

**Description:**  
A minimalistic solution where a single contract centrally manages all subdomains. Only the administrator can issue subdomains and manage their records. Suitable for simple use cases where ownership transfer is not required.

---

### `collection-contracts/`

[Contracts](collection-contracts) where subdomains are implemented as NFT items within a collection.

**Minting Types:**

- `admin-mint` — only the administrator can mint subdomains
- `paid-mint` — anyone can mint subdomains for a fixed fee
- `free-mint` — open and free minting for all users

**Description:**  
A more flexible approach where each subdomain is a distinct NFT. The collection contract serves as the subdomain manager. NFT owners have full control over their subdomains, including the ability to manage, transfer, or trade them.

---

### `metadata-api/`

An [API service](metadata-api) for generating images and metadata for subdomains and collections.

**Key Features:**

- Generates PNG images containing subdomain names
- Produces JSON metadata compatible with TON NFT standards

## License

This repository is licensed under the [MIT License](LICENSE).  
Feel free to use, modify, and distribute the code in accordance with the license terms.
