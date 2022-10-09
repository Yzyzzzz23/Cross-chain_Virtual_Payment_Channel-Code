# UTXO-based virtual channels

A small tool to create and evaluate the required transactions for UTXO-based virtual channels in Bitcoin 
for both a validity and non-validity construction.

## Usage:

- Install Python >= 3.7.3
- Install dependencies (check requirements.txt)
- execute main.py
- inspect the output to see raw transactions and size
- optional: enter different private keys and unspent TX outputs, publish resulting transactions on testnet
 
## Results:
This is the implementation of Bitcoin-compatible Virtual Channels.
    We build virtual channels (VC) over both Lightning Network (LN) [1] channels and Generalized channels (GC)[2].
    We offer two different VC constructions: (i) VC without validity (VC-NV)
(ii) VC with validity (VC-V); the latter ones have a pre-defined life-time

    The following measurements are observed from this implementation:
    Generalized channels:
        - 316 Split transaction with output for VC, TXa_NV (VC-NV)
        - 640 bytes TXf (VC-NV)
        - 309 bytes TXf (VC-V)
        ------
        - 280 Split transaction with output for VC, TXa_V (VC-V)
        - 377 bytes TXrefund (VC-V)
    Lightning channels:
        - 580 Commitment transaction with output for VC, CT_NV (VC-NV)
        - 640 bytes TXf (VC-NV)
        - 309 bytes TXf (VC-V)
        ------
        - 546 Commitment transaction with output for VC, CT_V (VC-V)
        - 377 bytes TXrefund (VC-V)
    -----------------------
    The following sizes are taken from [2] and their implementation
    (https://github.com/generalized-channels/gc):
    Generalized channels:
        - 431 bytes commitment transaction (1x per channel)
        - 264 bytes split transaction (1x per channel)
        - 387 bytes split with HTLC (1x per channel, no HTLC spend required)
    Lightning channels:
        - 353 bytes commitment transaction (2x per channel)
        - 514 bytes commitment transaction with 1 HTLC (2x per channel)
        - 249 bytes HTLC spend transaction (1 x per HTLC)
    -----------------------
    -----------------------
    -----------------------
    RESULTS (operation size in bytes):
    Generalized channels:
        - Open (NV): 2 * commitment + 2 * TXa_NV + TXf + commitment + split = 2829 (7 tx)
        - Open (V): 2 * commitment + 2 * TXa_NV + TXf + TX_refund + commitment + split = 2803 (8 tx)
        - UPDATE (NV & V): commitment + split = 695 (2 tx)
        - OFFLOAD (NV): 2 * commitment + 2 * TXa_NV + TXf = 2134
        - OFFLOAD (V): 2 * commitment + 2 * TXa_NV + TXf + TX_refund = 2108 (on-chain)
        - optimistic CLOSE (NV & V): 2 * (commitment + split) = 1390
        - pessimistic CLOSE (NV & V): same as Open, but on-chain
    Lightning channels:
        - Open (NV): 4 * CT_NV + 4 * TX_f + 8 * CT = 7704 (16 tx)
        - Open (V): 4 * CT_V + 2 * TX_f + 4 * TX_refund + 4 * CT = 5722 (14 tx)
        - UPDATE (NV): 8 * CT = 2824 (8 tx)
        - UPDATE (V): 4 * CT = 1412 (4 tx)
        - OFFLOAD (NV): 2 * CT_NV + TX_f = 1800 (3 tx)
        - OFFLOAD (V): 2 * CT_V + TX_f + TX_refund = 1778 (4 tx)
        - optimistic CLOSE (NV & V): 4 * CT = 1412 (4 tx)
        - pessimistic CLOSE (NV): OFFLOAD(NV) + CT = 2153 (4 tx)
        - pessimistic CLOSE (V): OFFLOAD(V) + CT = 2131 (5 tx)
    -----------------------
    Comparison to PCN:
        For 1 payment with VC:
        - CREATE + CLOSE
        For n sequential payments with VC:
        - CREATE + (n-1) * UPDATE + CLOSE
        or: CREATE - UPDATE + n * UPDATE + CLOSE
        ---
        GC-VC-NV: 3524+695*n
        GC-VC-V:  3498+695*n
        GC-PCN:   n * (2 * CT + 2 * Split_HTLC + 2 * CT + 2 * Split) = n * 3026
        ---
        LN-VC-NV: 6292+2824*n
        LN-VC-V:  4310+1412*n
        LN-PCN:   n * (4 * CT_HTLC + 4 * HTLC_SPEND + 4 * CT) = n * 4776

    [1] https://lightning.network/lightning-network-paper.pdf
    [2] https://eprint.iacr.org/2020/476.pdf
