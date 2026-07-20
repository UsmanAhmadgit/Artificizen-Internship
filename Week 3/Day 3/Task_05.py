#5.	Embed 50 random sentences, then query with a sentence that is semantically close but uses completely different words. Verify that semantic search still finds the right match.

from qdrant_client import QdrantClient, models  
from sentence_transformers import SentenceTransformer

def main():
    print("--- TASK 5: THE VOCABULARY DISCONNECT ---")
    
    encoder = SentenceTransformer('all-MiniLM-L6-v2')
    client = QdrantClient(":memory:")
    collection_name = "random_facts"
    
    client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE)
    )
    
    # A list of completely random sentences
    sentences = [
        "The chef chopped onions for the soup.",
        "My smartphone battery dies very quickly.",
        "The majestic eagle soars above the mountains.",
        "She painted the canvas with vibrant watercolors.",
        "Automobiles are accelerating faster than ever before.", # TARGET SENTENCE
        "The library is closed on public holidays.",
        "He drank a hot cup of coffee in the morning.",
        "A gentle breeze rustled the autumn leaves.",
        "Modern electric vehicles can reach high speeds rapidly.",
        "The quick brown fox jumps over the lazy dog.",
        "He prefers to read historical fiction before bed.",
        "Cybersecurity is essential for protecting sensitive data.",
        "The barista steamed milk for the cappuccino.",
        "Heavy rains caused flooding in the downtown area.",
        "Our team won the championship game last night.",
        "She planted tomatoes and basil in her garden.",
        "The stock market experienced a significant drop today.",
        "A new restaurant opened on the corner of Main Street.",
        "Artificial intelligence is reshaping software development.",
        "He strummed an acoustic guitar by the campfire.",
        "The museum features an exhibit on ancient Egypt.",
        "I need to upgrade my mobile device because it won't hold a charge.",
        "The children built a massive sandcastle on the beach.",
        "Space exploration aims to find habitable planets.",
        "A recipe for chocolate cake requires flour, eggs, and cocoa.",
        "The mechanic changed the oil and checked the tires.",
        "Yoga and meditation are great ways to reduce stress.",
        "They hiked a steep trail to reach the waterfall.",
        "The government passed a new law regarding renewable energy.",
        "He sketched a portrait using charcoal pencils.",
        "A flock of geese migrated south for the winter.",
        "The loud thunder startled the sleeping dog.",
        "Cryptocurrency prices fluctuate wildly on a daily basis.",
        "She booked a direct flight to Tokyo for her vacation.",
        "The software update fixed several critical bugs.",
        "Local farmers sell fresh produce at the weekend market.",
        "He practices playing the piano for two hours every day.",
        "The abandoned house at the end of the street is said to be haunted.",
        "Cooks often tear up when slicing pungent root vegetables.",
        "Public institutions usually lock their doors during national festivals.",
        "She knitted a warm woolen scarf for the winter.",
        "The biology textbook explains the process of photosynthesis.",
        "A traffic jam blocked the highway for over three hours.",
        "He captured a stunning photograph of the night sky.",
        "The company announced a merger with its biggest competitor.",
        "Astronauts undergo rigorous training before launching into space.",
        "The tailor stitched the hem of the silk dress.",
        "A large crowd gathered to watch the street performers.",
        "Wind turbines generate clean electricity from natural breezes.",
        "The detective uncovered a hidden clue at the crime scene."
    ]
    
    print("Uploading sentences...")
    points = [
        models.PointStruct(
            id=i,
            vector=encoder.encode(sentence).tolist(),
            payload={"text": sentence}
        )
        for i, sentence in enumerate(sentences)
    ]
    client.upsert(collection_name=collection_name, points=points)
    
    # Query uses entirely different words than the target
    query = "Cars are speeding up quicker nowadays."
    print(f"\nQuery: '{query}'")
    print("Notice how the query shares almost NO words with the target!\n")
    
    results = client.query_points(
        collection_name=collection_name,
        query=encoder.encode(query).tolist(),
        limit=1
    )
    
    print("Best Match Found:")
    best_match = results.points[0]
    print(f"Text: '{best_match.payload['text']}'")
    print(f"Similarity Score: {best_match.score:.4f}")

if __name__ == "__main__":
    main()
