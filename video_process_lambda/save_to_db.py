from db_init import CandidateVideoTranscriptions, init


async def save_to_db(file_id: str, text: str):
    # Client is bound to the event loop, and asyncio.run creates a new loop per invocation
    client = await init()
    try:
        candidate_video_transcription = await CandidateVideoTranscriptions.get(file_id)
        candidate_video_transcription.transcription = text
        await candidate_video_transcription.save()
    finally:
        await client.close()
