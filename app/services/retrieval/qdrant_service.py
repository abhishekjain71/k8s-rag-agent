import logfire
from qdrant_client import QdrantClient
from qdrant_client.http import models
from app.config import settings
from app.services.retrieval.embeddings import embed_query

from tenacity import retry, stop_after_attempt, before_sleep_log, wait_exponential

## initialize the Qdrant Client--
client= QdrantClient(
    url=settings.QDRANT_URL,
    api_key=settings.QDRANT_API_KEY
)


# @retry(
#     stop= stop_after_attempt(3),
#     wait= wait_exponential(multiplier=1, min=1, max=5),
#     reraise= True,
#     before_sleep= before_sleep_log(logfire, "Warning")
# )
def search_enterprise_knowledge(query: str, limit: int=8):
    """ 
    Performs a high -precision search in the enterprise knowledge base.
    Uses the modern query_points interface.
    """
    try:
        query_vector= embed_query(query)
        
        ## using query_points -- the modern standard for qdrant ## in old client.search()
        response= client.query_points(
            collection_name=settings.QDRANT_COLLECTION,
            query=query_vector,
            limit=limit,
            with_payload=True ## JSON attach metaData
        )
        
        results=[]
        
        for res in response.points:
            results.append({
                "content" : res.payload.get("text",""),
                "source": res.payload.get("source","Unknown"),
                "score": res.score
                
            })
            
        return results
    except Exception as e:
        logfire.error(f"Qdrant search Failed : {e}")
        return []
