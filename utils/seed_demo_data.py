import os
import logging
from pathlib import Path
from config.settings import DEMO_DIR, UPLOADS_DIR
from core.document_processor import DocumentProcessor
from core.vector_store import global_vector_store
from database.models import DocumentModel

logger = logging.getLogger(__name__)

DEMO_MATERIALS = {
    "Operating_Systems_Core.txt": """
# CHAPTER: OPERATING SYSTEMS & DEADLOCK MANAGEMENT

## 1. Deadlock Definition
A deadlock is an undesirable state in operating systems where two or more processes are permanently blocked because each process holds a resource that another process needs, creating a circular dependency.

## 2. Four Necessary Conditions for Deadlock (Coffman Conditions)
For a deadlock to occur, all four Coffman conditions must hold simultaneously:
1. Mutual Exclusion: At least one resource must be held in a non-shareable mode.
2. Hold and Wait: A process must hold at least one resource while waiting to acquire additional resources held by other processes.
3. No Preemption: Resources cannot be forcibly taken away from a process; they can only be released voluntarily after completion.
4. Circular Wait: A closed chain of processes exists such that each process holds one or more resources needed by the next process in the chain.

## 3. Deadlock Handling Strategies
- Deadlock Prevention: Eliminates at least one of the four necessary conditions during design.
- Deadlock Avoidance: Uses resource allocation state algorithms (such as Dijkstra's Banker's Algorithm) to dynamically inspect whether granting a resource request leaves the system in a safe state.
- Deadlock Detection and Recovery: Allows the system to enter a deadlock, periodically runs a detection algorithm (Wait-For Graph), and recovers by process termination or resource preemption.

## 4. CPU Scheduling Algorithms
- First-Come, First-Served (FCFS): Non-preemptive, suffers from the Convoy Effect.
- Shortest Job First (SJF): Optimal average waiting time, but requires knowing execution time in advance.
- Round Robin (RR): Preemptive scheduling with a fixed time quantum, ideal for time-sharing systems.
""",
    "Database_Management_Systems.txt": """
# CHAPTER: DATABASE MANAGEMENT SYSTEMS & NORMALIZATION

## 1. Purpose of Database Normalization
Normalization is a systematic technique of organizing data in a relational database to reduce data redundancy and eliminate undesirable anomalies such as Insertion Anomaly, Deletion Anomaly, and Update Anomaly.

## 2. Normal Forms Breakdown
- First Normal Form (1NF): Requires that all attributes contain atomic (indivisible) values and every column contains unique values. No repeating groups allowed.
- Second Normal Form (2NF): Must be in 1NF and all non-key attributes must be fully functionally dependent on the primary key. Eliminates Partial Dependencies.
- Third Normal Form (3NF): Must be in 2NF and no non-key attribute is transitively dependent on the primary key. Eliminates Transitive Dependencies (X -> Y and Y -> Z).
- Boyce-Codd Normal Form (BCNF): A stricter version of 3NF where for every functional dependency X -> Y, X must be a super key.

## 3. ACID Properties in Database Transactions
- Atomicity: Ensures that all operations in a transaction complete successfully or all are rolled back. (All or Nothing).
- Consistency: Ensures that the database transitions from one valid state to another valid state, preserving constraints.
- Isolation: Ensures that concurrent execution of transactions leaves the database in the same state as if executed sequentially.
- Durability: Guarantees that once a transaction commits, its updates persist permanently even during system crashes.
""",
    "Computer_Networks_Protocols.txt": """
# CHAPTER: COMPUTER NETWORKS & TRANSPORT PROTOCOLS

## 1. OSI 7-Layer Reference Model vs TCP/IP
The Open Systems Interconnection (OSI) reference model categorizes network protocols into 7 layers:
1. Physical Layer: Bitstream transmission over physical media.
2. Data Link Layer: Framing, MAC addressing, and error detection (Ethernet, Wi-Fi).
3. Network Layer: Logical IP addressing and packet routing across routers.
4. Transport Layer: End-to-end communication, error recovery, flow control (TCP, UDP).
5. Session Layer: Session establishment and maintenance.
6. Presentation Layer: Data encryption, compression, and format conversion.
7. Application Layer: User application protocols (HTTP, FTP, SMTP, DNS).

## 2. TCP vs UDP Protocols
- Transmission Control Protocol (TCP): Connection-oriented, reliable, guarantees packet ordering via 3-way handshake (SYN, SYN-ACK, ACK), incorporates sliding window flow control and congestion window algorithms.
- User Datagram Protocol (UDP): Connectionless, lightweight, unreliable, low-latency protocol suitable for streaming, DNS, and real-world gaming.
""",
    "Generative_AI_Architecture.txt": """
# CHAPTER: GENERATIVE AI & RAG ARCHITECTURES

## 1. Transformer Neural Network Architecture
Transformers (Vaswani et al., 2017) revolutionized Natural Language Processing by replacing recurrent neural networks (RNNs) with Self-Attention mechanisms.
- Scaled Dot-Product Attention computes query-key matrix multiplication to assign dynamic weights to word representations.
- Multi-Head Attention allows the model to jointly attend to information from different representation subspaces.
- Positional Encodings inject sequential order without relying on recurrent loops.

## 2. Retrieval-Augmented Generation (RAG)
RAG combines non-parametric vector memory with parametric Large Language Models (LLMs) to eliminate hallucinations and provide verifiable source citations.
1. Document Chunking: Breaking text into contextual chunks.
2. Embeddings: Mapping chunks into a high-dimensional vector space using sentence transformers.
3. Similarity Search: Querying FAISS/Chroma vector DB to find top-K context passages.
4. Prompt Augmentation: Feeding retrieved context into the LLM context window.
"""
}

def seed_demo_data_if_needed():
    """Seeds CS study files if vector store or DB is empty."""
    existing_docs = DocumentModel.get_all_documents()
    if len(existing_docs) > 0 and global_vector_store.get_chunk_count() > 0:
        return

    logger.info("Seeding CS Demo Data into StudyMind...")
    for fname, content in DEMO_MATERIALS.items():
        file_path = DEMO_DIR / fname
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        # Process and chunk
        processed = DocumentProcessor.process_and_chunk(file_path)
        doc_id = DocumentModel.add_document(
            filename=fname,
            file_type="txt",
            file_size=len(content),
            page_count=processed["page_count"],
            chunk_count=len(processed["chunks"]),
            topics=["Computer Science", fname.split("_")[0]],
            summary={"Executive Summary": content[:200] + "..."}
        )

        # Add to vector store
        global_vector_store.add_chunks(doc_id, fname, processed["chunks"])
        # Add to DB chunks
        DocumentModel.add_chunks(doc_id, processed["chunks"])

    logger.info("Demo data seeding completed successfully.")

if __name__ == "__main__":
    seed_demo_data_if_needed()
